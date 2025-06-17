# utils/embedder.py

from openai import OpenAI
import os
import time

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key="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")

def openai_embed(text, model="text-embedding-3-small", max_retries=3):
    """
    Generate a semantic embedding using OpenAI's embedding model (SDK v1+).
    """
    text = text.replace("\n", " ")

    for attempt in range(max_retries):
        try:
            response = client.embeddings.create(
                model=model,
                input=[text]
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"[Retry {attempt+1}] OpenAI API error: {e}")
            time.sleep(1)

    return None
