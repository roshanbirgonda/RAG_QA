# sync_verified_to_chroma.py

from utils.memory_store import get_verified_answers
from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(anonymized_telemetry=False))
collection = client.get_or_create_collection("long_term_verified")

verified_data = get_verified_answers()

if not verified_data:
    print("❌ No verified answers to sync.")
else:
    for i, qa in enumerate(verified_data):
        collection.add(
            documents=[qa["answer"]],
            metadatas=[{
                "question": qa["question"],
                "source": "long_term",
                "type": "verified_answer"
            }],
            ids=[f"verified_{i}"]
        )
    print(f"✅ Synced {len(verified_data)} verified answers to ChromaDB.")
