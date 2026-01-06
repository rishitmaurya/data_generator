import json
import re

def clean(text):
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

all_tasks = []

for file in [
    "scraped_data/github_tasks_raw.json",
    "scraped_data/jira_tasks_raw.json"
]:
    with open(file, encoding="utf-8") as f:
        for t in json.load(f):
            if len(t["name"]) < 8 or len(t["description"]) < 20:
                continue
            all_tasks.append({
                "name": clean(t["name"]),
                "description": clean(t["description"])
            })

with open("scraped_data/task_corpus.json", "w", encoding="utf-8") as f:
    json.dump(all_tasks, f, indent=2)

print(f"Saved {len(all_tasks)} realistic tasks")
