import gradio as gr
from utils.memory_store import add_to_memory
from sync_verified_to_chroma import get_verified_answers
from openai import OpenAI
from dotenv import load_dotenv
import os
import chromadb

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(path="./vector_db")
collection = chroma_client.get_or_create_collection("docs")

def embed_query(text):
    response = client.embeddings.create(model="text-embedding-3-small", input=[text])
    return response.data[0].embedding

def retrieve_and_answer(query, feedback, correction):
    embed = embed_query(query)
    results = collection.query(query_embeddings=[embed], n_results=5, include=["documents"])
    context = "\n\n".join(results["documents"][0])
    prompt = f"Context:\n{context}\n\nQ: {query}\nA:"

    answer = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content.strip()

    fb = "thumbs_up" if feedback == "👍" else "thumbs_down"
    add_to_memory(query, answer, fb, correction if fb == "thumbs_down" else None)

    if fb == "thumbs_up":
        get_verified_answers()

    return answer

ui = gr.Interface(
    fn=retrieve_and_answer,
    inputs=[
        gr.Textbox(label="Your Question"),
        gr.Radio(["👍", "👎"], label="Feedback"),
        gr.Textbox(label="Correction (if any)", lines=2)
    ],
    outputs="text",
    title="Document Q&A System with Feedback"
)

ui.launch()
