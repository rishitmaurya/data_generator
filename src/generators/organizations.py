import uuid
from datetime import datetime

def generate_organization(conn, context):
    """
    Generates 1 organization for the simulation
    """
    org_id = str(uuid.uuid4())
    name = "Acme SaaS Inc."  # realistic company name
    domain = "acme.com"
    created_at = datetime.now()

    # Insert into DB
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO organizations (organization_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (org_id, name, domain, created_at)
    )
    conn.commit()

    # Update context
    context["organization_id"] = org_id
    print(f"[Organization] Created: {name} ({org_id})")
