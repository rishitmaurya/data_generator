import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from utils.config import COMMENT_PROBABILITY, COMMENT_MIN_DAYS, COMMENT_MAX_DAYS

fake = Faker()
random.seed(42)

def generate_comments(conn, context):
    cursor = conn.cursor()
    total_comments = 0

    for task_id, task in context["tasks"].items():
        # Chance task has comments
        if random.random() > COMMENT_PROBABILITY:
            continue

        team_users = task.get("team_users", [])
        num_comments = random.randint(1, 5)
        total_comments += num_comments

        # Convert task created_at to datetime if string
        task_created_at = task["created_at"]
        if isinstance(task_created_at, str):
            task_created_at = datetime.fromisoformat(task_created_at)

        for _ in range(num_comments):
            comment_id = str(uuid.uuid4())
            author_id = random.choice(team_users) if team_users and random.random() > 0.1 else None  # some comments can have no author
            comment_type = 'user' if random.random() > 0.05 else 'system'
            content = fake.paragraph(nb_sentences=random.randint(1,3))

            # Temporal consistency: comment after task creation
            created_at = task_created_at + timedelta(days=random.randint(COMMENT_MIN_DAYS, COMMENT_MAX_DAYS))
            if "due_date" in task and task["due_date"]:
                created_at = min(created_at, task["due_date"])  # comments shouldn't appear after task due date

            cursor.execute("""
                INSERT INTO comments (comment_id, task_id, author_id, comment_type, content, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (comment_id, task_id, author_id, comment_type, content, created_at))

    conn.commit()
    print(f"[Comments] Generated approx {total_comments} comments")
