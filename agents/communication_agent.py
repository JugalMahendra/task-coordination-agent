import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'mcp_servers', 'communication_tools'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from communication_tools import send_notification, send_reminder, send_encouragement

def notify_task_assigned(user_id, task_title):
    return send_notification(user_id, f"You have been assigned: {task_title}")

def remind_overdue(user_id, task_title):
    return send_reminder(user_id, task_title, f"Reminder: {task_title} is due soon")

def encourage_performer(user_id, message):
    return send_encouragement(user_id, message)
