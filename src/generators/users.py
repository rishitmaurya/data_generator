import uuid
from faker import Faker
from datetime import datetime
from utils.config import TOTAL_USERS

fake = Faker()

def generate_users(conn, context):
    """
    Generate realistic users for the organization
    """
    cursor = conn.cursor()
    org_id = context["organization_id"]
    user_ids = []

    for i in range(TOTAL_USERS):
        user_id = str(uuid.uuid4())
        full_name = fake.name()

        # Make email unique: combine name slug + index + short UUID
        name_slug = full_name.lower().replace(" ", ".")
        email = f"{name_slug}.{i+1}.{uuid.uuid4().hex[:6]}@example.com"

        job_title = fake.job()
        is_active = 1
        joined_at = fake.date_time_between(start_date='-6M', end_date='now')
        created_at = joined_at

        cursor.execute(
            """
            INSERT INTO users (user_id, organization_id, full_name, email, job_title, is_active, joined_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (user_id, org_id, full_name, email, job_title, is_active, joined_at, created_at)
        )

        user_ids.append(user_id)

    conn.commit()
    context["users"] = {"all": user_ids}
    print(f"[Users] Generated {len(user_ids)} users")
