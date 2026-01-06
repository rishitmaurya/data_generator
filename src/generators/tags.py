import uuid
import random

TAG_POOL_SIZE = 75  # Number of tags to generate

def generate_tags(conn, context):
    cursor = conn.cursor()
    tags = []

    # Generate tags
    for _ in range(TAG_POOL_SIZE):
        tag_id = str(uuid.uuid4())
        name = f"Tag {uuid.uuid4().hex[:6]}"  # simple unique tag name
        cursor.execute("INSERT INTO tags (tag_id, name) VALUES (?, ?)", (tag_id, name))
        tags.append(tag_id)

    # Assign tags to tasks
    for task_id in context["tasks"]:
        num_tags = random.randint(0, 5)
        assigned_tags = random.sample(tags, k=min(num_tags, len(tags)))
        for tag_id in assigned_tags:
            cursor.execute("INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)", (task_id, tag_id))

    conn.commit()
    context["tags"] = tags
    print(f"[Tags] Generated {len(tags)} tags and assigned to tasks")
