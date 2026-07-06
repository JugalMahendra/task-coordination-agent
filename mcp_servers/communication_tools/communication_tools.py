def send_notification(user_id, message):
    return {"user_id": user_id, "message": message, "status": "sent"}

def send_reminder(user_id, task_id, message):
    return {"user_id": user_id, "task_id": task_id, "message": message, "status": "reminder_sent"}

def send_encouragement(user_id, message):
    return {"user_id": user_id, "message": message, "type": "encouragement", "status": "sent"}
