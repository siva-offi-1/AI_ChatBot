from pathlib import Path
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MarkdownRetriever:
    def __init__(self, documents_dir, top_k=4, threshold=0.12, chunk_size=1200):
        self.documents_dir = Path(documents_dir)
        self.top_k, self.threshold, self.chunk_size = top_k, threshold, chunk_size
        self.chunks, self.vectorizer, self.matrix = [], None, None

    def _chunk_file(self, text, source):
        chunks, section, buffer = [], "Introduction", []
        def flush():
            raw = "\n".join(buffer).strip()
            if not raw:
                return
            parts, current = re.split(r"\n\s*\n", raw), ""
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                if current and len(current) + len(part) + 2 > self.chunk_size:
                    chunks.append({"source": source, "section": section, "content": current})
                    current = part
                else:
                    current = (current + "\n\n" + part).strip()
            if current:
                chunks.append({"source": source, "section": section, "content": current})
        for line in text.splitlines():
            if line.startswith("#"):
                flush()
                buffer = []
                section = line.lstrip("#").strip() or "Untitled"
            else:
                buffer.append(line)
        flush()
        return chunks

    def load_documents(self):
        if not self.documents_dir.exists():
            raise FileNotFoundError(f"Documents folder not found: {self.documents_dir}")
        self.chunks = []
        for path in sorted(self.documents_dir.glob("*.md")):
            self.chunks.extend(self._chunk_file(path.read_text(encoding="utf-8"), path.name))
        if not self.chunks:
            raise ValueError("No Markdown documents found in documents folder")
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([c["content"] for c in self.chunks])
        return len(self.chunks)

    def search(self, question):
        if self.matrix is None:
            raise RuntimeError("Documents are not loaded")
        q = self.vectorizer.transform([question])
        scores = cosine_similarity(q, self.matrix).flatten()
        indexes = scores.argsort()[::-1][:self.top_k]
        return [
            {**self.chunks[i], "score": float(scores[i])}
            for i in indexes if scores[i] >= self.threshold
        ]
