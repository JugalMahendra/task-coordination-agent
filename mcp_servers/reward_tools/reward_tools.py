import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from seed_demo import TASKS_ASSIGNMENT, get_task, get_user, get_points_balance, get_available_rewards

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
