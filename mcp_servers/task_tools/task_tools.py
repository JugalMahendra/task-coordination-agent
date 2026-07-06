import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from seed_demo import TASKS, TASKS_ASSIGNMENT, get_task, get_user

def list_tasks(taskStatus=None):
    if taskStatus is None:
        return TASKS
    else:
        result = []
        for task in TASKS:
            if taskStatus == task["status"]:
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
