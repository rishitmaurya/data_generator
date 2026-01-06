import os
import random
from utils.db import get_connection
from utils.config import RANDOM_SEED
from generators.organizations import generate_organization
from generators.users import generate_users
from generators.teams import generate_teams
from generators.team_memberships import generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections
from generators.tasks import generate_tasks
from generators.tags import generate_tags
from generators.comments import generate_comments
from generators.attachments import generate_attachments
from generators.fields import generate_custom_fields
# Optional: verification script
# from utils.verify import verify_relational_integrity


def apply_schema(conn, schema_file="schema.sql"):
    """
    Apply schema.sql to create all tables
    """
    if not os.path.exists(schema_file):
        raise FileNotFoundError(f"{schema_file} not found!")

    with open(schema_file, "r", encoding="utf-8") as f:
        sql = f.read()
    conn.executescript(sql)
    print("[Schema] Applied schema.sql successfully.")


def clear_database(conn):
    """
    Drop all tables before regeneration
    """
    cursor = conn.cursor()
    tables = [
        'task_tags', 'tags', 'custom_field_values', 'custom_field_definitions',
        'attachments', 'comments', 'tasks', 'sections', 'projects',
        'team_memberships', 'teams', 'users', 'organizations'
    ]
    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")
    conn.commit()
    print("[Database] Cleared existing tables.")


def populate_context(conn, context):
    """
    Load projects, tasks, and task-team info into context dictionary.
    Required for Step 9 generators (tags, comments, attachments, custom fields)
    """
    cursor = conn.cursor()

    # Load all projects
    cursor.execute("SELECT project_id, team_id FROM projects")
    projects = cursor.fetchall()
    context["projects"] = [p[0] for p in projects]
    project_team_map = {p[0]: p[1] for p in projects}

    # Load all tasks with created_at and project_id
    cursor.execute("SELECT task_id, project_id, created_at FROM tasks")
    tasks_data = cursor.fetchall()
    tasks_dict = {}
    for t in tasks_data:
        task_id, project_id, created_at = t
        team_id = project_team_map.get(project_id)
        # Load users of the team
        cursor.execute("SELECT user_id FROM team_memberships WHERE team_id = ?", (team_id,))
        team_users = [u[0] for u in cursor.fetchall()]
        tasks_dict[task_id] = {
            "project_id": project_id,
            "created_at": created_at,
            "team_users": team_users
        }
    context["tasks"] = tasks_dict


def main():
    # Seed for reproducibility
    random.seed(RANDOM_SEED)

    conn = get_connection()

    # Optional: clear database before generating
    # clear_database(conn)

    # Step 1: Apply schema
    apply_schema(conn)

    # Initialize context (shared across generators)
    context = {}

    # Step 6: Organization + Users
    generate_organization(conn, context)
    generate_users(conn, context)
    print("Step 6 complete: Organization + Users generated.")

    # Step 7: Teams + Team Memberships
    generate_teams(conn, context)
    generate_team_memberships(conn, context)
    print("Step 7 complete: Teams + Team Memberships generated.")

    # Step 8: Projects, Sections, Tasks
    generate_projects(conn, context)
    generate_sections(conn, context)
    generate_tasks(conn, context)
    print("Step 8 complete: Projects, Sections, and Tasks generated.")

    # ✅ Populate context with tasks + projects before Step 9
    populate_context(conn, context)

    # Step 9: Tags, Comments, Attachments, Custom Fields
    generate_tags(conn, context)
    generate_comments(conn, context)
    generate_attachments(conn, context)
    generate_custom_fields(conn, context)
    print("Step 9 complete: Comments, Attachments, Tags, Custom Fields generated.")

    # Step 10: Optional verification of relational integrity
    # verify_relational_integrity(conn)
    # print("Step 10 complete: Relational integrity verified.")

    conn.close()
    print("[Database] Generation completed successfully.")


if __name__ == "__main__":
    main()
