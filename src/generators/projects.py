import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from utils.config import TOTAL_PROJECTS, HISTORY_MONTHS

fake = Faker()

PROJECT_TYPES = [
    'engineering_sprint', 'bug_tracking', 'product_roadmap',
    'marketing_campaign', 'customer_success', 'operations'
]

def generate_projects(conn, context):
    cursor = conn.cursor()
    teams = context["teams"]
    users = context["users"]["all"]  # list of all user_ids
    project_ids = []

    projects_per_team = TOTAL_PROJECTS // len(teams)

    for team_id in teams:
        for _ in range(projects_per_team):
            project_id = str(uuid.uuid4())
            org_id = context["organization_id"]
            owner_id = random.choice(users)
            project_type = random.choice(PROJECT_TYPES)
            name = f"{project_type.replace('_',' ').title()} - {fake.bs().title()}"
            status = random.choices(['active','archived'], weights=[0.8,0.2])[0]
            created_at = fake.date_time_between(start_date=f'-{HISTORY_MONTHS}M', end_date='now')
            archived_at = None
            if status == 'archived':
                archived_at = created_at + timedelta(days=random.randint(30,90))
            updated_at = datetime.now() if status == 'active' else archived_at

            cursor.execute("""
                INSERT INTO projects 
                (project_id, organization_id, team_id, owner_id, name, project_type, status, created_at, updated_at, archived_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (project_id, org_id, team_id, owner_id, name, project_type, status, created_at, updated_at, archived_at))

            project_ids.append(project_id)

    conn.commit()
    context["projects"] = project_ids
    print(f"[Projects] Generated {len(project_ids)} projects")
