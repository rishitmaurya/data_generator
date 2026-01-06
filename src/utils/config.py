# src/utils/config.py

import random

# ------------------------------
# General Organization Settings
# ------------------------------
TOTAL_USERS = 7800           # Total number of users in the simulated organization
TOTAL_TEAMS = 90             # Total number of teams
TOTAL_PROJECTS = 750         # Total number of projects
HISTORY_MONTHS = 6           # Simulation time range (for created_at, joined_at etc.)
RANDOM_SEED = 42             # Random seed for reproducibility

# ------------------------------
# Task Settings
# ------------------------------
TASKS_PER_PROJECT_MIN = 10
TASKS_PER_PROJECT_MAX = 20

SUBTASK_PROBABILITY = 0.3    # 30% of tasks will have subtasks
SUBTASKS_MIN = 1
SUBTASKS_MAX = 5

OVERDUE_TASK_PROBABILITY = 0.05      # 5% tasks will be overdue
UNASSIGNED_TASK_PROBABILITY = 0.15   # 15% tasks will have no assignee
EMPTY_PROJECT_PROBABILITY = 0.1      # 10% projects will have zero tasks

# ------------------------------
# Tags Configuration
# ------------------------------
TAG_POOL_SIZE = 75               # Total number of tags
TAG_ASSIGN_MIN = 0               # Minimum tags per task
TAG_ASSIGN_MAX = 5               # Maximum tags per task

# ------------------------------
# Custom Fields Configuration
# ------------------------------
CUSTOM_FIELDS_PER_PROJECT_MIN = 1
CUSTOM_FIELDS_PER_PROJECT_MAX = 5

# ------------------------------
# Temporal / Date Settings
# ------------------------------
# Days range for due dates
DUE_DATE_MIN_DAYS = 1
DUE_DATE_MAX_DAYS = 90

# Days range for task completion after creation
COMPLETION_MIN_DAYS = 1
COMPLETION_MAX_DAYS = 14

# Days range for subtasks after parent task creation
SUBTASK_MIN_OFFSET_DAYS = 0
SUBTASK_MAX_OFFSET_DAYS = 7


# Comments
COMMENT_PROBABILITY = 0.7
COMMENT_MIN_DAYS = 0
COMMENT_MAX_DAYS = 14

# Attachments
ATTACHMENT_PROBABILITY = 0.3
ATTACHMENT_MIN_DAYS = 0
ATTACHMENT_MAX_DAYS = 14
