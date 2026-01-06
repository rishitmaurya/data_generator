Here’s a comprehensive **README.md** tailored for your project structure, installation, usage, and connectivity explanation:

---

# **Asana Simulation Data Generator**

This project generates **high-quality seed data** simulating an Asana workspace for a B2B SaaS company with 5,000–10,000 users. The dataset can be used for **reinforcement learning experiments, testing AI agents**, or evaluating enterprise workflows.

---

## **Project Structure**

```
├── .gitignore
├─] env/ (ignored)
├── output/
│   └── asana_simulation.sqlite
├── requirements.txt
├── schema.sql
└── src/
    ├── generators/
    │   ├── attachments.py
    │   ├── comments.py
    │   ├── fields.py
    │   ├── organizations.py
    │   ├── projects.py
    │   ├── sections.py
    │   ├── tags.py
    │   ├── tasks.py
    │   ├── teams.py
    │   ├── team_memberships.py
    │   ├── users.py
    │   ├── __init__.py
    │   └── __pycache__/
    │       ├── attachments.cpython-312.pyc
    │       ├── comments.cpython-312.pyc
    │       ├── fields.cpython-312.pyc
    │       ├── organizations.cpython-312.pyc
    │       ├── projects.cpython-312.pyc
    │       ├── sections.cpython-312.pyc
    │       ├── tags.cpython-312.pyc
    │       ├── tasks.cpython-312.pyc
    │       ├── teams.cpython-312.pyc
    │       ├── team_memberships.cpython-312.pyc
    │       ├── users.cpython-312.pyc
    │       └── __init__.cpython-312.pyc
    ├── main.py
    ├── utils/
    │   ├── config.py
    │   ├── db.py
    │   ├── __init__.py
    │   └── __pycache__/
    │       ├── config.cpython-312.pyc
    │       ├── db.cpython-312.pyc
    │       ├── llm.cpython-312.pyc
    │       └── __init__.cpython-312.pyc
    ├── __init__.py
    └── __pycache__/
        ├── main.cpython-312.pyc
        └── __init__.cpython-312.pyc
```

---

## **Installation Instructions**

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/asana_simulation.git
cd c:/programming/asana_simulation/data_generator/
```

### 2. Set up Virtual Environment

```bash
python -m venv env
```

### 3. Activate Virtual Environment

**Windows:**

```bash
env\Scripts\activate
```

**Linux / MacOS:**

```bash
source env/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies include:**

* `Faker` — for realistic names, emails, and text content
* `uuid` — for generating unique identifiers
* `sqlite3` — built-in module for SQLite database interaction
* `random` and `datetime` — for realistic distributions and timestamps

---

## **Database Connectivity**

1. The project uses **SQLite** to store generated data in `output/asana_simulation.sqlite`.
2. Connection is handled via `src/utils/db.py`:

```python
import sqlite3
from pathlib import Path

def get_connection(db_path="output/asana_simulation.sqlite"):
    Path("output").mkdir(exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
```

3. All generators (`users`, `tasks`, `projects`, `comments`, `attachments`, etc.) **accept a connection object** and a **context dictionary** for dependency management.

---

## **Running the Data Generator**

```bash
python src/main.py
```

**Process Steps Executed:**

1. **Schema Setup**

   * Creates all tables in SQLite from `schema.sql`
   * Enforces foreign keys and indexes for performance

2. **Generate Organizations & Users**

   * Single organization
   * 5,000–10,000 users with realistic names, emails, and job titles

3. **Generate Teams & Memberships**

   * Teams with 5–50 users
   * Roles: `member`, `lead`, `admin`

4. **Generate Projects, Sections, Tasks**

   * Projects categorized by type (engineering, marketing, etc.)
   * Standardized sections (`To Do`, `In Progress`, `Done`)
   * Tasks and subtasks with realistic names, descriptions, and due dates

5. **Generate Tags, Comments, Attachments, Custom Fields**

   * Tags applied to tasks (0–5 per task)
   * Comments: 1–5 per task, authored by team members
   * Attachments: 0–3 per task, realistic file types
   * Custom fields per project with type-specific values

6. **Populate SQLite Database**

   * All data saved to `output/asana_simulation.sqlite`
   * Referential and temporal integrity guaranteed

---

## **Configuration**

All key constants are stored in `src/utils/config.py`:

```python
TOTAL_USERS = 7800
TOTAL_TEAMS = 90
TOTAL_PROJECTS = 750
TASKS_PER_PROJECT_MIN = 10
TASKS_PER_PROJECT_MAX = 20
SUBTASK_PROBABILITY = 0.3
COMMENT_PROBABILITY = 0.7
ATTACHMENT_PROBABILITY = 0.3
OVERDUE_TASK_PROBABILITY = 0.05
UNASSIGNED_TASK_PROBABILITY = 0.15
EMPTY_PROJECT_PROBABILITY = 0.1
HISTORY_MONTHS = 6
RANDOM_SEED = 42
```

**Adjust these values** to scale the dataset up or down for experiments.

---

## **Output**

* **SQLite Database**: `output/asana_simulation.sqlite`
* Tables include:

  * `organizations`, `users`, `teams`, `team_memberships`
  * `projects`, `sections`, `tasks`, `comments`, `attachments`
  * `tags`, `task_tags`, `custom_field_definitions`, `custom_field_values`

---

## **Code Conventions**

* Modular design: Each generator handles a single entity type
* **Context dictionary**: Passes dependencies between generators (e.g., tasks → comments)
* Temporal consistency and referential integrity enforced for RL realism
* Seeded randomization ensures reproducible datasets

