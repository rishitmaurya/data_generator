import uuid
from datetime import datetime

SECTIONS = ["To Do", "In Progress", "Done"]

def generate_sections(conn, context):
    cursor = conn.cursor()
    sections_map = {}

    for project_id in context["projects"]:
        sections_map[project_id] = []
        for position, name in enumerate(SECTIONS):
            section_id = str(uuid.uuid4())
            created_at = datetime.now()
            cursor.execute("""
                INSERT INTO sections (section_id, project_id, name, position, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (section_id, project_id, name, position, created_at))
            sections_map[project_id].append(section_id)

    conn.commit()
    context["sections"] = sections_map
    print(f"[Sections] Created sections for all projects")
