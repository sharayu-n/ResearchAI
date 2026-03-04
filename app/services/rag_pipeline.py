from app.services.retriever import Retriever
from app.services.llm_service import LLMService
import textwrap

MAX_CHARS_PER_CONTEXT = 1000  # trim very long chunks for prompt safety


class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.llm = LLMService()

    def _build_prompt(self, question: str, contexts):
        """
        contexts: list of dicts from Retriever with keys chunk_id, distance, score, text
        We build a numbered context section and provide clear instructions.
        """
        # create numbered, trimmed context entries
        entries = []
        for i, c in enumerate(contexts, start=1):
            excerpt = c["text"]
            if len(excerpt) > MAX_CHARS_PER_CONTEXT:
                excerpt = excerpt[:MAX_CHARS_PER_CONTEXT].rsplit(" ", 1)[0] + "..."
            # sanitize whitespace a little
            excerpt = " ".join(excerpt.split())
            entries.append(f"[{i}] (chunk_id={c['chunk_id']}, score={c['score']:.3f})\n{excerpt}")

        context_text = "\n\n".join(entries)

        prompt = f"""
            You are a document extraction assistant. Create a concise answer to the question based ONLY on the provided contexts. 

            Strict rules:
            - Only use the provided context blocks.
            - You can combine information from multiple blocks if needed, but do NOT assume anything not explicitly stated.
            - Give big answers if the question is complex, but do NOT add any information that is not directly supported by the context.
            - Do NOT infer.
            - Do NOT add commentary.
            - If asked to list items, return a clean bullet list only.
            - If information is missing, respond exactly: "Not found in document."

            Context blocks:
            ----------------
            {context_text}
            ----------------

            Question:
            {question}

            Answer:
            """

        return prompt
    
    def generate_overview(self, num_chunks: int = 8):
        # take first N chunks (usually contains title + abstract)
        contexts = self.retriever.chunks[:num_chunks]

        context_text = "\n\n".join(contexts)

        prompt = f"""
    You are a research assistant.

    Summarize the following research paper in 5-6 concise lines.
    Do not add extra commentary.
    

    Text:
    ----------------
    {context_text}
    ----------------

    Summary:
    """

        summary = self.llm.generate(prompt)

        return {
            "overview": summary.strip()
        }

    def generate_answer(self, question: str, k: int = 5):
        contexts = self.retriever.retrieve(question, k=k)

        # build the prompt from only the 'text' fields (but include meta in the prompt display)
        prompt = self._build_prompt(question, contexts)

        # call the LLM
        answer = self.llm.generate(prompt)

        # prepare structured citations (map block numbers back to chunk_id, distance)
        citations = []
        for i, c in enumerate(contexts, start=1):
            citations.append({
                "block": i,
                "chunk_id": c["chunk_id"],
                "distance": c["distance"],
                "score": c["score"],
                "excerpt": (c["text"][:300] + "...") if len(c["text"]) > 300 else c["text"]
            })

        return {
            "answer": answer.strip(),
            "citations": citations,
            "raw_prompt": prompt  # keep for debugging; remove in production if you prefer
        }