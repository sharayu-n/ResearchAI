import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

class LLMService:
    def generate(self, prompt: str) -> str:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(OLLAMA_URL, json=payload)

        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.text}")

        return response.json()["response"]