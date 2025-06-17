import re

def semantic_chunk(text, max_len=500):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if len(current_chunk) + len(para) < max_len:
            current_chunk += " " + para
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def sliding_window_chunk(text, window_size=500, overlap=100):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+window_size]
        chunks.append(" ".join(chunk))
        i += window_size - overlap
    return chunks
