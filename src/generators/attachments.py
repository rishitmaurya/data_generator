import uuid
import random
from datetime import timedelta, datetime

FILE_TYPES = ['pdf', 'docx', 'xlsx', 'png', 'jpg']

def generate_attachments(conn, context):
    cursor = conn.cursor()
    total_attachments = 0

    for task_id in context["tasks"]:
        # 30% of tasks get attachments
        if random.random() > 0.3:
            continue

        num_attachments = random.randint(1, 3)
        total_attachments += num_attachments
        task = context["tasks"][task_id]
        team_users = task.get("team_users", [])

        # Convert task created_at to datetime
        task_created_at = task["created_at"]
        if isinstance(task_created_at, str):
            task_created_at = datetime.fromisoformat(task_created_at)

        for _ in range(num_attachments):
            attachment_id = str(uuid.uuid4())
            uploaded_by = random.choice(team_users) if team_users else None
            file_type = random.choice(FILE_TYPES)
            file_name = f"{uuid.uuid4().hex[:6]}.{file_type}"

            # Add a random offset of 0-14 days
            uploaded_at = task_created_at + timedelta(days=random.randint(0,14))

            cursor.execute("""
                INSERT INTO attachments (attachment_id, task_id, uploaded_by, file_name, file_type, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (attachment_id, task_id, uploaded_by, file_name, file_type, uploaded_at.isoformat()))

    conn.commit()
    print(f"[Attachments] Generated approx {total_attachments} attachments")
