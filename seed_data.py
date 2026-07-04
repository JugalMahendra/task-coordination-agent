"""
Fake family data for the Task Coordination Agent.
No database needed — just dictionaries.

Modify this to match your own family or a pretend one.
"""

FAMILY = {
    "members": [
        {"id": "mom", "name": "Mom", "role": "parent", "age": 35},
        {"id": "dad", "name": "Dad", "role": "parent", "age": 37},
        {"id": "emma", "name": "Emma", "role": "child", "age": 12},
        {"id": "john", "name": "John", "role": "child", "age": 10},
        {"id": "lily", "name": "Lily", "role": "child", "age": 8},
    ]
}

TASKS = [
    {
        "id": "task_1",
        "title": "Wash dishes",
        "difficulty": "easy",
        "points": 20,
        "status": "pending",
        "due_date": "2026-06-26",
    },
    {
        "id": "task_2",
        "title": "Take out trash",
        "difficulty": "easy",
        "points": 10,
        "status": "pending",
        "due_date": "2026-06-26",
    },
    {
        "id": "task_3",
        "title": "Vacuum living room",
        "difficulty": "medium",
        "points": 30,
        "status": "pending",
        "due_date": "2026-06-27",
    },
    {
        "id": "task_4",
        "title": "Clean bathroom",
        "difficulty": "hard",
        "points": 50,
        "status": "pending",
        "due_date": "2026-06-27",
    },
    {
        "id": "task_5",
        "title": "Mow the lawn",
        "difficulty": "hard",
        "points": 60,
        "status": "pending",
        "due_date": "2026-06-28",
    },
    {
        "id": "task_6",
        "title": "Set the table",
        "difficulty": "easy",
        "points": 10,
        "status": "pending",
        "due_date": "2026-06-26",
    },
]

TASKS_ASSIGNMENT = [
    {"user_id": "emma", "task_id": "task_1", "status": "completed", "date": "2026-06-24"},
    {"user_id": "emma", "task_id": "task_3", "status": "completed", "date": "2026-06-23"},
    {"user_id": "john", "task_id": "task_2", "status": "completed", "date": "2026-06-24"},
    {"user_id": "john", "task_id": "task_5", "status": "completed", "date": "2026-06-22"},
    {"user_id": "lily", "task_id": "task_6", "status": "completed", "date": "2026-06-24"},
    {"user_id": "lily", "task_id": "task_1", "status": "failed", "date": "2026-06-23"},
    {"user_id": "mom", "task_id": "task_4", "status": "completed", "date": "2026-06-24"},
    {"user_id": "dad", "task_id": "task_5", "status": "completed", "date": "2026-06-23"},
]

def get_task(task_id):
    for task in TASKS:
        if task["id"] == task_id:
            return task
    return None


def get_pending_tasks():
    """Return only tasks that haven't been assigned yet."""
    pending = []
    for task in TASKS:
        if task["status"] == "pending":
            pending.append(task)
    return pending


def get_user(user_id):
    """Get a single user by ID."""
    for member in FAMILY["members"]:
        if member["id"] == user_id:
            return member
    return None

def get_task_assignee(user_id, task_id):
    """Get a single task assignee by ID."""
    history = []
    for entry in TASKS_ASSIGNMENT:
        if entry["user_id"] == user_id and entry["task_id"] == task_id:
            history.append(entry)
    return history

def get_completions_for_user(user_id):
    """Get completion history for a specific person."""
    history = []
    for entry in TASKS_ASSIGNMENT:
        if entry["user_id"] == user_id:
            history.append(entry)
    return history


def get_available_rewards():
    """Return a list of rewards a kid can redeem points for."""
    return [
        {"name": "30 min screen time", "cost": 50},
        {"name": "Ice cream treat", "cost": 30},
        {"name": "Stay up 30 min late", "cost": 40},
        {"name": "Choose dinner", "cost": 60},
    ]


def get_points_balance(user_id):
    """Calculate how many points a user has from completed tasks."""
    total = 0
    for entry in TASKS_ASSIGNMENT:
        if entry["user_id"] == user_id and entry["status"] == "completed":
            # Find the task to get its point value
            for task in TASKS:
                if task["id"] == entry["task_id"]:
                    total = total + task["points"]
    return total


if __name__ == "__main__":
    print("=== Family Members ===")
    for member in FAMILY["members"]:
        print(f"  {member['name']} ({member['role']}, age {member['age']})")

    print("\n=== Pending Tasks ===")
    pending_tasks = get_pending_tasks()
    for task in pending_tasks:
        print(f"  {task['title']} — {task['difficulty']} ({task['points']} pts)")

    print("\n=== Emma's History ===")
    emma_history = get_completions_for_user("emma")
    for entry in emma_history:
        print(f"  {entry['task_id']}: {entry['status']}")

    print("\n=== Points Balance ===")
    for member in FAMILY["members"]:
        balance = get_points_balance(member["id"])
        print(f"  {member['name']}: {balance} points")
