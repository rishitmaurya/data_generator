import uuid
import random
from datetime import datetime, timedelta
from utils.config import ATTACHMENT_PROBABILITY, ATTACHMENT_MIN_DAYS, ATTACHMENT_MAX_DAYS

FILE_TYPES = ['pdf', 'docx', 'xlsx', 'png', 'jpg']
random.seed(42)

def generate_attachments(conn, context):
    cursor = conn.cursor()
    total_attachments = 0

    for task_id, task in context["tasks"].items():
        # Chance task has attachments
        if random.random() > ATTACHMENT_PROBABILITY:
            continue

        team_users = task.get("team_users", [])
        num_attachments = random.randint(1, 3)
        total_attachments += num_attachments

        # Convert task created_at to datetime if string
        task_created_at = task["created_at"]
        if isinstance(task_created_at, str):
            task_created_at = datetime.fromisoformat(task_created_at)

        for _ in range(num_attachments):
            attachment_id = str(uuid.uuid4())
            uploaded_by = random.choice(team_users) if team_users else None
            file_type = random.choice(FILE_TYPES)
            file_name = f"{uuid.uuid4().hex[:6]}.{file_type}"

            # Temporal consistency: upload after task creation
            uploaded_at = task_created_at + timedelta(days=random.randint(ATTACHMENT_MIN_DAYS, ATTACHMENT_MAX_DAYS))
            if "due_date" in task and task["due_date"]:
                uploaded_at = min(uploaded_at, task["due_date"])  # attachments shouldn't appear after task due date

            cursor.execute("""
                INSERT INTO attachments (attachment_id, task_id, uploaded_by, file_name, file_type, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (attachment_id, task_id, uploaded_by, file_name, file_type, uploaded_at))

    conn.commit()
    print(f"[Attachments] Generated approx {total_attachments} attachments")
