import chromadb

client = chromadb.PersistentClient(path="./vector_db")
collection = client.get_or_create_collection(name="docs")

# ✅ Correct usage
results = collection.get(include=["documents", "metadatas"])

# Print stored chunks and metadata
for idx in range(len(results["ids"])):
    print(f"\n🧩 Chunk ID: {results['ids'][idx]}")
    print(f"📄 Document Text:\n{results['documents'][idx]}...")  # Preview only
    print(f"🗂️ Metadata: {results['metadatas'][idx]}")
