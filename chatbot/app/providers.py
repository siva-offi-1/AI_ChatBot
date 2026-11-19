from openai import OpenAI

class OpenAIAnswerProvider:
    def __init__(self, api_key, model):
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Add it to .env")
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, question, context):
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content":
                 "You are Northstar Holdings' policy assistant. Answer only from the supplied document context. "
                 "Do not invent information or use outside knowledge. If the answer is not in the context, say: "
                 "'The available documents do not provide the answer.' Mention the source document names."},
                {"role": "user", "content": f"DOCUMENT CONTEXT:\n{context}\n\nQUESTION:\n{question}"}
            ]
        )
        return response.choices[0].message.content or "The available documents do not provide the answer."
