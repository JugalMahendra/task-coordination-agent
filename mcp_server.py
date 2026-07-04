from seed_data import TASKS, TASKS_ASSIGNMENT, get_task, get_user, get_points_balance, get_available_rewards

def list_tasks(taskStatus=None) :
    if taskStatus is None:
        return TASKS
    else:
        result = []
        for task in TASKS :
            if taskStatus == task["status"] :
                result.append(task)
        return result

def assign_task(task_id, user_id, due_date, reason=None):
    task = get_task(task_id)
    if task is None:
        return f"Task with {task_id} Not Found"
    if get_user(user_id) is None:
        return f"User with {user_id} Not Found"

    task = {"task_id": task["id"], "user_id": user_id, "reason": reason, "status": "assigned", "due_date": due_date}
    TASKS_ASSIGNMENT.append(task)
    return task


def get_user_capacity(user_id):
    return len([a for a in TASKS_ASSIGNMENT if a["user_id"] == user_id and a["status"] == "assigned"])


def get_engagement_metrics(user_id):
    user = get_user(user_id)
    if user is None:
        return f"User with {user_id} Not Found"
    
    total_assigned = len([a for a in TASKS_ASSIGNMENT if a["user_id"] == user_id])
    completed = len([a for a in TASKS_ASSIGNMENT if a["user_id"] == user_id and a["status"] == "completed"])
    failed = len([a for a in TASKS_ASSIGNMENT if a["user_id"] == user_id and a["status"] == "failed"])
    points = get_points_balance(user_id)
    capacity = get_user_capacity(user_id)
    
    completion_rate = (completed / total_assigned * 100) if total_assigned > 0 else 0
    
    return {
        "user_id": user_id,
        "name": user["name"],
        "total_assigned": total_assigned,
        "completed": completed,
        "failed": failed,
        "completion_rate": round(completion_rate, 1),
        "points_balance": points,
        "current_capacity": capacity
    }


def suggest_reward(user_id):
    user = get_user(user_id)
    if user is None:
        return f"User with {user_id} Not Found"
    
    points = get_points_balance(user_id)
    rewards = get_available_rewards()
    
    affordable = [r for r in rewards if r["cost"] <= points]
    
    return {
        "user_id": user_id,
        "name": user["name"],
        "points_balance": points,
        "affordable_rewards": affordable,
        "suggestion": affordable[-1] if affordable else None
    }


def update_points_ledger(user_id, task_id, status):
    user = get_user(user_id)
    if user is None:
        return f"User with {user_id} Not Found"
    
    task = get_task(task_id)
    if task is None:
        return f"Task with {task_id} Not Found"
    
    for entry in TASKS_ASSIGNMENT:
        if entry["user_id"] == user_id and entry["task_id"] == task_id:
            entry["status"] = status
            return entry
    
    return f"No assignment found for user {user_id} on task {task_id}"
