# memory_store.py

import json
import os
import uuid
from datetime import datetime

MEMORY_FILE = "memory_log.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory_data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4)

def add_to_memory(question, answer, feedback=None, corrected_answer=None):
    memory_data = load_memory()
    new_entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "feedback": feedback,  # thumbs_up or thumbs_down
        "corrected_answer": corrected_answer
    }
    memory_data.append(new_entry)
    save_memory(memory_data)
    return new_entry

def get_verified_answers():
    memory_data = load_memory()
    return [entry for entry in memory_data if entry.get("feedback") == "thumbs_up"]
