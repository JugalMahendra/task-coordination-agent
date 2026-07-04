list_task = {
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "Get all tasks, optionally filtered by status (pending, assigned, completed)",
        "parameters": {
            "type": "object",
            "properties": {
                "taskStatus": {
                    "type": "string",
                    "description": "Filter by status: pending, assigned, or completed"
                }
            },
            "required": []
        }
    }
}

assign_task = {
    "type": "function",
    "function": {
        "name": "assign_task",
        "description": "assign the task to a user and set status as assigned. The user need to mention the end date and can optionally mention reason",
        "parameters": {
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "string",
                    "description": "id of the task to be assigned"
                },
                "user_id": {
                    "type": "string",
                    "description": "id of the user to be assigned"
                },
                "due_date": {
                    "type": "string",
                    "description": "date the user need to finish the task. the format needs to be 'YYYY-MM-DD'"
                },
                "reason": {
                    "type": "string",
                    "description": "reason to assign the task"
                }
            },
            "required": ["task_id", "user_id", "due_date"]
        }
    }
}

get_user_capacity = {
    "type": "function",
    "function": {
        "name": "get_user_capacity",
        "description": "get user's capacity",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "id of the user to be checked"
                }
            },
            "required": ["user_id"]
        }
    }
}

get_engagement_metrics = {
    "type": "function",
    "function": {
        "name": "get_engagement_metrics",
        "description": "Get engagement metrics for a family member - completion rate, points, and task load",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "id of the user to check metrics for"
                }
            },
            "required": ["user_id"]
        }
    }
}

suggest_reward = {
    "type": "function",
    "function": {
        "name": "suggest_reward",
        "description": "Suggest a reward the user can afford based on their points balance",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "id of the user to suggest rewards for"
                }
            },
            "required": ["user_id"]
        }
    }
}

update_points_ledger = {
    "type": "function",
    "function": {
        "name": "update_points_ledger",
        "description": "Update the status of a task assignment (completed, failed, in_progress)",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "id of the user"
                },
                "task_id": {
                    "type": "string",
                    "description": "id of the task to update"
                },
                "status": {
                    "type": "string",
                    "description": "new status: completed, failed, or in_progress"
                }
            },
            "required": ["user_id", "task_id", "status"]
        }
    }
}
