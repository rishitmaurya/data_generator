PRAGMA foreign_keys = ON;

--------------------------------------------------
-- ORGANIZATION / WORKSPACE
--------------------------------------------------
CREATE TABLE IF NOT EXISTS organizations (
    organization_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);

--------------------------------------------------
-- USERS
--------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    job_title TEXT,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    joined_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

--------------------------------------------------
-- TEAMS
--------------------------------------------------
CREATE TABLE IF NOT EXISTS teams (
    team_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    is_active INTEGER NOT NULL DEFAULT 1 CHECK (is_active IN (0,1)),
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

--------------------------------------------------
-- TEAM MEMBERSHIPS (Many-to-Many)
--------------------------------------------------
CREATE TABLE IF NOT EXISTS team_memberships (
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT CHECK (role IN ('member', 'lead', 'admin')) NOT NULL,
    joined_at TIMESTAMP NOT NULL,
    PRIMARY KEY (team_id, user_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

--------------------------------------------------
-- PROJECTS
--------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
    project_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    team_id TEXT,
    owner_id TEXT,
    name TEXT NOT NULL,
    project_type TEXT CHECK (
        project_type IN (
            'engineering_sprint',
            'bug_tracking',
            'product_roadmap',
            'marketing_campaign',
            'customer_success',
            'operations'
        )
    ) NOT NULL,
    status TEXT CHECK (status IN ('active', 'archived')) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    archived_at TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

--------------------------------------------------
-- SECTIONS
--------------------------------------------------
CREATE TABLE IF NOT EXISTS sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

--------------------------------------------------
-- TASKS (Includes Subtasks via parent_task_id)
--------------------------------------------------
CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    section_id TEXT,
    parent_task_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    created_by TEXT,
    assignee_id TEXT,
    due_date DATE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0,1)),
    completed_at TIMESTAMP,
    is_archived INTEGER NOT NULL DEFAULT 0 CHECK (is_archived IN (0,1)),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

--------------------------------------------------
-- COMMENTS / STORIES
--------------------------------------------------
CREATE TABLE IF NOT EXISTS comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    author_id TEXT,
    comment_type TEXT CHECK (comment_type IN ('user', 'system')) NOT NULL DEFAULT 'user',
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (author_id) REFERENCES users(user_id)
);

--------------------------------------------------
-- ATTACHMENTS
--------------------------------------------------
CREATE TABLE IF NOT EXISTS attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    uploaded_by TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);

--------------------------------------------------
-- CUSTOM FIELD DEFINITIONS
--------------------------------------------------
CREATE TABLE IF NOT EXISTS custom_field_definitions (
    custom_field_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    field_type TEXT CHECK (field_type IN ('text', 'number', 'enum')) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

--------------------------------------------------
-- CUSTOM FIELD VALUES
--------------------------------------------------
CREATE TABLE IF NOT EXISTS custom_field_values (
    task_id TEXT NOT NULL,
    custom_field_id TEXT NOT NULL,
    value_text TEXT,
    value_number REAL,
    value_enum TEXT,
    PRIMARY KEY (task_id, custom_field_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (custom_field_id) REFERENCES custom_field_definitions(custom_field_id)
);

--------------------------------------------------
-- TAGS
--------------------------------------------------
CREATE TABLE IF NOT EXISTS tags (
    tag_id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

--------------------------------------------------
-- TASK <-> TAG ASSOCIATION
--------------------------------------------------
CREATE TABLE IF NOT EXISTS task_tags (
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);

--------------------------------------------------
-- INDEXES (Performance & RL realism)
--------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_users_org ON users(organization_id);

CREATE INDEX IF NOT EXISTS idx_projects_org ON projects(organization_id);
CREATE INDEX IF NOT EXISTS idx_projects_team ON projects(team_id);
CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id);

CREATE INDEX IF NOT EXISTS idx_sections_project ON sections(project_id);

CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_assignee ON tasks(assignee_id);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
CREATE INDEX IF NOT EXISTS idx_tasks_parent ON tasks(parent_task_id);

CREATE INDEX IF NOT EXISTS idx_comments_task ON comments(task_id);
