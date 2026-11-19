import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from app.config import Settings
from app.retrieval import MarkdownRetriever
from app.providers import OpenAIAnswerProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
settings = Settings()
retriever = MarkdownRetriever(settings.DOCUMENTS_DIR, settings.TOP_K, settings.RETRIEVAL_THRESHOLD)
provider = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    count = retriever.load_documents()
    logger.info("Indexed %s chunks from Markdown documents", count)
    yield

app = FastAPI(title="Northstar Holdings AI Policy Assistant", lifespan=lifespan)

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.get("/health")
def health():
    return {"status": "healthy", "indexed_chunks": len(retriever.chunks)}

@app.post("/ask")
def ask(request: AskRequest):
    global provider
    results = retriever.search(request.question)
    if not results:
        return {"answer": "The available documents do not provide the answer.",
                "sources": [], "grounded": False}
    context = "\n\n".join(
        f"Source: {r['source']}\nSection: {r['section']}\nContent:\n{r['content']}"
        for r in results
    )
    mode = "openai"
    try:
        if provider is None:
            provider = OpenAIAnswerProvider(settings.OPENAI_API_KEY, settings.OPENAI_MODEL)
        answer = provider.generate(request.question, context)
    except Exception as e:
        # Keep the policy assistant useful when the OpenAI API is unavailable
        # (for example, when API billing/quota is exhausted). Return only text
        # retrieved from the policy documents; never invent an answer.
        logger.exception("OpenAI API request failed; using document-only fallback")
        mode = "document_fallback"
        answer = "I couldn't generate an AI-formatted response, so here is the relevant information found in the policy documents:\n\n" + "\n\n".join(
            f"**{r['source']} — {r['section']}**\n{r['content']}" for r in results
        )
    sources = [{"document": r["source"], "section": r["section"],
                "relevance": round(r["score"], 4)} for r in results]
    return {"answer": answer, "sources": sources, "grounded": True, "mode": mode}
