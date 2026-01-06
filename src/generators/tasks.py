import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from utils.config import TASKS_PER_PROJECT_MIN, TASKS_PER_PROJECT_MAX

fake = Faker()

def generate_tasks(conn, context):
    cursor = conn.cursor()
    users_by_team = context["users"]["by_team"]

    total_tasks = 0
    for project_id in context["projects"]:
        # Get team_id for this project
        cursor.execute("SELECT team_id FROM projects WHERE project_id=?", (project_id,))
        team_id = cursor.fetchone()[0]
        team_users = users_by_team.get(team_id, [])

        num_tasks = random.randint(TASKS_PER_PROJECT_MIN, TASKS_PER_PROJECT_MAX)
        total_tasks += num_tasks

        for _ in range(num_tasks):
            task_id = str(uuid.uuid4())
            section_id = random.choice(context["sections"][project_id])
            name = fake.sentence(nb_words=6)
            description = fake.paragraph(nb_sentences=3)
            created_by = random.choice(team_users) if team_users else None
            assignee_id = random.choice(team_users) if team_users and random.random() > 0.15 else None
            due_date = datetime.now() + timedelta(days=random.randint(1,90))
            created_at = datetime.now() - timedelta(days=random.randint(1,180))
            updated_at = created_at + timedelta(days=random.randint(0,30))
            completed = 1 if random.random() < 0.6 else 0
            completed_at = created_at + timedelta(days=random.randint(1,14)) if completed else None

            cursor.execute("""
                INSERT INTO tasks 
                (task_id, project_id, section_id, name, description, created_by, assignee_id, due_date, created_at, updated_at, completed, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, project_id, section_id, name, description, created_by, assignee_id, due_date, created_at, updated_at, completed, completed_at))

    conn.commit()
    print(f"[Tasks] Generated approx {total_tasks} tasks across all projects")
