import json
import random
from pathlib import Path

DATA_PATH = Path("scraped_data/task_corpus.json")

with open(DATA_PATH, encoding="utf-8") as f:
    TASK_POOL = json.load(f)

def get_task_text():
    task = random.choice(TASK_POOL)
    return task["name"], task["description"]
