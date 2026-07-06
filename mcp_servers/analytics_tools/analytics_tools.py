import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from seed_demo import TASKS_ASSIGNMENT, get_user, get_points_balance

def get_engagement_metrics(user_id):
    user = get_user(user_id)
    if user is None:
        return f"User with {user_id} Not Found"
    
    total_assigned = len([a for a in TASKS_ASSIGNMENT if a["user_id"] == user_id])
    completed = len([a for a in TASKS_ASSIGNMENT if a["user_id"] == user_id and a["status"] == "completed"])
    failed = len([a for a in TASKS_ASSIGNMENT if a["user_id"] == user_id and a["status"] == "failed"])
    points = get_points_balance(user_id)
    
    completion_rate = (completed / total_assigned * 100) if total_assigned > 0 else 0
    
    return {
        "user_id": user_id,
        "name": user["name"],
        "total_assigned": total_assigned,
        "completed": completed,
        "failed": failed,
        "completion_rate": round(completion_rate, 1),
        "points_balance": points
    }
