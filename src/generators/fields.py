import uuid
import random
from datetime import datetime
from utils.config import CUSTOM_FIELDS_PER_PROJECT_MIN, CUSTOM_FIELDS_PER_PROJECT_MAX

FIELD_TYPES = ['text', 'number', 'enum']

def generate_custom_fields(conn, context):
    cursor = conn.cursor()

    for project_id in context["projects"]:
        # Random number of fields per project
        num_fields = random.randint(CUSTOM_FIELDS_PER_PROJECT_MIN, CUSTOM_FIELDS_PER_PROJECT_MAX)
        custom_fields = []

        for _ in range(num_fields):
            custom_field_id = str(uuid.uuid4())
            name = f"CF {uuid.uuid4().hex[:5]}"
            field_type = random.choice(FIELD_TYPES)
            created_at = datetime.now()

            cursor.execute("""
                INSERT INTO custom_field_definitions (custom_field_id, project_id, name, field_type, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (custom_field_id, project_id, name, field_type, created_at))
            custom_fields.append({"id": custom_field_id, "type": field_type})

        # Assign values for all tasks in the project
        project_tasks = [tid for tid, t in context["tasks"].items() if t["project_id"] == project_id]
        for task_id in project_tasks:
            for field in custom_fields:
                value_text = value_number = value_enum = None
                if field["type"] == "text":
                    value_text = f"Value {uuid.uuid4().hex[:4]}"
                elif field["type"] == "number":
                    value_number = round(random.uniform(1,100), 2)
                elif field["type"] == "enum":
                    value_enum = random.choice(["Option A", "Option B", "Option C"])

                cursor.execute("""
                    INSERT INTO custom_field_values (task_id, custom_field_id, value_text, value_number, value_enum)
                    VALUES (?, ?, ?, ?, ?)
                """, (task_id, field["id"], value_text, value_number, value_enum))

    conn.commit()
    print("[Custom Fields] Created fields and assigned values")
