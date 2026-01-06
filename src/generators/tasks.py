import uuid
import random
from datetime import datetime, timedelta
from faker import Faker
from utils.config import (
    TASKS_PER_PROJECT_MIN, TASKS_PER_PROJECT_MAX,
    SUBTASK_PROBABILITY, SUBTASKS_MIN, SUBTASKS_MAX,
    OVERDUE_TASK_PROBABILITY, UNASSIGNED_TASK_PROBABILITY,
    EMPTY_PROJECT_PROBABILITY,
    DUE_DATE_MIN_DAYS, DUE_DATE_MAX_DAYS,
    COMPLETION_MIN_DAYS, COMPLETION_MAX_DAYS,
    SUBTASK_MIN_OFFSET_DAYS, SUBTASK_MAX_OFFSET_DAYS
)
from utils.task_text_provider import get_task_text


fake = Faker()
random.seed(42)

def generate_tasks(conn, context):
    cursor = conn.cursor()
    users_by_team = context["users"]["by_team"]

    total_tasks = 0
    for project_id in context["projects"]:
        # 10% chance this project has zero tasks
        if random.random() < EMPTY_PROJECT_PROBABILITY:
            continue

        # Get team_id for this project
        cursor.execute("SELECT team_id FROM projects WHERE project_id=?", (project_id,))
        team_id = cursor.fetchone()[0]
        team_users = users_by_team.get(team_id, [])

        num_tasks = random.randint(TASKS_PER_PROJECT_MIN, TASKS_PER_PROJECT_MAX)
        total_tasks += num_tasks

        for _ in range(num_tasks):
            task_id = str(uuid.uuid4())
            section_id = random.choice(context["sections"][project_id])
            name, description = get_task_text()
            # name = fake.sentence(nb_words=6)
            # description = fake.paragraph(nb_sentences=3)
            
            # Assign created_by and assignee with edge case probabilities
            created_by = random.choice(team_users) if team_users else None
            assignee_id = None
            if team_users and random.random() > UNASSIGNED_TASK_PROBABILITY:
                assignee_id = random.choice(team_users)

            # Temporal fields
            created_at = datetime.now() - timedelta(days=random.randint(0, 180))
            due_date = created_at + timedelta(days=random.randint(DUE_DATE_MIN_DAYS, DUE_DATE_MAX_DAYS))
            if random.random() < OVERDUE_TASK_PROBABILITY:
                due_date = created_at - timedelta(days=random.randint(1, 14))  # overdue

            updated_at = created_at + timedelta(days=random.randint(0, 30))
            completed = 1 if random.random() < 0.6 else 0
            completed_at = created_at + timedelta(days=random.randint(COMPLETION_MIN_DAYS, COMPLETION_MAX_DAYS)) if completed else None

            cursor.execute("""
                INSERT INTO tasks 
                (task_id, project_id, section_id, name, description, created_by, assignee_id, due_date, created_at, updated_at, completed, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, project_id, section_id, name, description, created_by, assignee_id, due_date, created_at, updated_at, completed, completed_at))

            # --- Subtask generation ---
            if random.random() < SUBTASK_PROBABILITY:
                num_subtasks = random.randint(SUBTASKS_MIN, SUBTASKS_MAX)
                for _ in range(num_subtasks):
                    subtask_id = str(uuid.uuid4())
                    parent_name = name
                    subtask_name = f"{parent_name.split()[0]} subtask"
                    subtask_description = f"Part of: {parent_name}. {description[:120]}"

                    # subtask_name = fake.sentence(nb_words=5)
                    # subtask_description = fake.paragraph(nb_sentences=2)
                    subtask_assignee = random.choice(team_users) if team_users and random.random() > UNASSIGNED_TASK_PROBABILITY else None
                    subtask_created_at = created_at + timedelta(days=random.randint(SUBTASK_MIN_OFFSET_DAYS, SUBTASK_MAX_OFFSET_DAYS))
                    subtask_updated_at = subtask_created_at + timedelta(days=random.randint(0, 7))
                    subtask_completed = 1 if random.random() < 0.5 else 0
                    subtask_completed_at = subtask_created_at + timedelta(days=random.randint(COMPLETION_MIN_DAYS, COMPLETION_MAX_DAYS)) if subtask_completed else None

                    cursor.execute("""
                        INSERT INTO tasks 
                        (task_id, project_id, section_id, parent_task_id, name, description, created_by, assignee_id, due_date, created_at, updated_at, completed, completed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        subtask_id, project_id, section_id, task_id, subtask_name, subtask_description,
                        created_by, subtask_assignee, due_date, subtask_created_at, subtask_updated_at,
                        subtask_completed, subtask_completed_at
                    ))

    conn.commit()
    print(f"[Tasks] Generated approx {total_tasks} tasks across all projects")
