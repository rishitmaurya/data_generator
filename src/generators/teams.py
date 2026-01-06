import uuid
from faker import Faker
from datetime import datetime
from utils.config import TOTAL_TEAMS, HISTORY_MONTHS
import random

fake = Faker()

DEPARTMENTS = ['Engineering', 'Marketing', 'Product', 'Customer Success', 'Operations']

def generate_teams(conn, context):
    """
    Generates teams for the organization and updates context
    """
    cursor = conn.cursor()
    org_id = context["organization_id"]
    team_ids = []

    for _ in range(TOTAL_TEAMS):
        team_id = str(uuid.uuid4())
        department = random.choice(DEPARTMENTS)
        name = f"{department} - {fake.word().capitalize()} Team"
        created_at = fake.date_time_between(start_date=f'-{HISTORY_MONTHS}M', end_date='now')

        cursor.execute(
            """
            INSERT INTO teams (team_id, organization_id, name, department, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (team_id, org_id, name, department, created_at)
        )
        team_ids.append(team_id)

    conn.commit()
    context["teams"] = team_ids
    print(f"[Teams] Generated {len(team_ids)} teams")
