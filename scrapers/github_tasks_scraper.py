import requests
import json

REPOS = [
    "django/django",
    "pallets/flask",
    "kubernetes/kubernetes",
    "facebook/react"
]

GITHUB_API = "https://api.github.com"

def scrape():
    tasks = []

    for repo in REPOS:
        for page in range(1, 4):  # limit pages
            url = f"{GITHUB_API}/repos/{repo}/issues"
            params = {"state": "all", "per_page": 100, "page": page}
            r = requests.get(url, params=params)

            if r.status_code != 200:
                break

            for issue in r.json():
                if "pull_request" in issue:
                    continue

                if not issue["body"]:
                    continue

                tasks.append({
                    "name": issue["title"].strip(),
                    "description": issue["body"].strip()
                })

    with open("scraped_data/github_tasks_raw.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

if __name__ == "__main__":
    scrape()
