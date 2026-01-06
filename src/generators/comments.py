from datetime import datetime, timedelta
import uuid
import random
from faker import Faker

fake = Faker()

def generate_comments(conn, context):
    cursor = conn.cursor()
    total_comments = 0

    for task_id in context["tasks"]:
        # 50-80% chance task has comments
        if random.random() > 0.8:
            continue

        num_comments = random.randint(1, 5)
        total_comments += num_comments

        for _ in range(num_comments):
            comment_id = str(uuid.uuid4())
            task = context["tasks"][task_id]
            team_users = task.get("team_users", [])
            author_id = random.choice(team_users) if team_users else None
            comment_type = 'user' if random.random() > 0.05 else 'system'
            content = fake.paragraph(nb_sentences=random.randint(1,3))

            # --- Fix: convert string to datetime if needed ---
            task_created_at = task["created_at"]
            if isinstance(task_created_at, str):
                task_created_at = datetime.fromisoformat(task_created_at)

            created_at = task_created_at + timedelta(days=random.randint(0,14))

            cursor.execute("""
                INSERT INTO comments (comment_id, task_id, author_id, comment_type, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (comment_id, task_id, author_id, comment_type, content, created_at.isoformat()))

    conn.commit()
    print(f"[Comments] Generated approx {total_comments} comments")
