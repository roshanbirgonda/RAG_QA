from utils.parser import extract_text
from utils.chunker import semantic_chunk
# from utils.embedder import mock_embed
from utils.embedder import openai_embed
from utils.vector_store import store_chunks
import uuid
import os

def process_document(path):
    print(f"\n📄 Processing: {path}")
    text = extract_text(path)

    chunks = semantic_chunk(text, max_len=500)
    print(f"✂️  Chunked into {len(chunks)} chunks")

    embeddings = [openai_embed(chunk) for chunk in chunks]

    metadata_list = [{
        "id": str(uuid.uuid4()),
        "source": os.path.basename(path),
        "chunk_index": i
    } for i in range(len(chunks))]

    store_chunks(chunks, embeddings, metadata_list)
    print("✅ Stored in vector DB")

if __name__ == "__main__":
    # Change this to your actual file path
    process_document("samples/sample_doc.txt")
