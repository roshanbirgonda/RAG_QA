# phase_2.py

import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

# Load environment variables from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./vector_db")
collection = chroma_client.get_or_create_collection("docs")

# Step 1: Embed the query
def embed_query(query, model="text-embedding-3-small"):
    response = client.embeddings.create(
        model=model,
        input=[query]
    )
    return response.data[0].embedding

# Step 2: Retrieve relevant chunks
def retrieve_relevant_chunks(query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )
    return results

# Step 3: Build prompt from context
def build_prompt(query, retrieved_chunks):
    context = "\n\n".join(retrieved_chunks["documents"][0])
    prompt = f"""You are a helpful assistant. Use the context below to answer the question.

Context:
{context}

Question: {query}
Answer:"""
    return prompt

# Step 4: Get answer from OpenAI GPT
def get_openai_response(prompt, model="gpt-4"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Run the full pipeline
def ask_question(query):
    print(f"\n🔍 Question: {query}")
    
    query_embedding = embed_query(query)
    print("🔎 Retrieved relevant chunks from vector DB...")
    
    retrieved = retrieve_relevant_chunks(query_embedding)
    
    prompt = build_prompt(query, retrieved)
    print("🧠 Constructed prompt with context...")

    answer = get_openai_response(prompt)
    
    print("\n✅ Final Answer:")
    print(answer)
    return answer

# CLI test
if __name__ == "__main__":
    user_question = input("Ask your question: ")
    ask_question(user_question)
