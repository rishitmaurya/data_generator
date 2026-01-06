import random
from datetime import datetime
from faker import Faker

fake = Faker()
ROLES = ['member', 'lead', 'admin']

def generate_team_memberships(conn, context):
    """
    Assign users to teams and populate team_memberships table
    """
    cursor = conn.cursor()
    users = context["users"]["all"]
    teams = context["teams"]
    team_members = {}  # will update context

    remaining_users = users.copy()
    random.shuffle(remaining_users)

    for team_id in teams:
        # Realistic team size: 5-15 users
        team_size = random.randint(5, 15)
        if len(remaining_users) < team_size:
            team_members_list = remaining_users
            remaining_users = []
        else:
            team_members_list = remaining_users[:team_size]
            remaining_users = remaining_users[team_size:]

        team_members[team_id] = team_members_list

        for i, user_id in enumerate(team_members_list):
            # First member is team lead (if team has >1 member), rest are 'member'
            role = 'lead' if i == 0 else 'member'
            joined_at = fake.date_time_between(start_date='-6M', end_date='now')
            cursor.execute(
                """
                INSERT INTO team_memberships (team_id, user_id, role, joined_at)
                VALUES (?, ?, ?, ?)
                """,
                (team_id, user_id, role, joined_at)
            )

    conn.commit()
    context["users"]["by_team"] = team_members
    print(f"[Team Memberships] Assigned users to {len(teams)} teams")
