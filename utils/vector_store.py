# utils/vector_store.py

import chromadb

# ✅ new-style Chroma client
client = chromadb.PersistentClient(path="./vector_db")

# Create or get the collection
collection = client.get_or_create_collection(name="docs")

def store_chunks(chunks, embeddings, metadata_list):
    for chunk, embedding, metadata in zip(chunks, embeddings, metadata_list):
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[metadata["id"]]
        )
