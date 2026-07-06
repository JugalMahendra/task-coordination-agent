import json
import os
from datetime import datetime

MEMORY_DIR = os.path.join(os.path.dirname(__file__))
SHARED_MEMORY_FILE = os.path.join(MEMORY_DIR, "shared_memory.json")

def load_shared_memory():
    try:
        with open(SHARED_MEMORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "orchestrator_messages": [],
            "motivator_messages": [],
            "assignments": [],
            "created_at": str(datetime.now())
        }

def save_shared_memory(state):
    def serialize_messages(msgs):
        serialized = []
        for m in msgs:
            if isinstance(m, dict):
                serialized.append(m)
            elif hasattr(m, '__dict__'):
                serialized.append(m.__dict__)
            else:
                serialized.append(str(m))
        return serialized
    
    state_to_save = state.copy()
    if "orchestrator_messages" in state_to_save:
        state_to_save["orchestrator_messages"] = serialize_messages(state_to_save["orchestrator_messages"])
    if "motivator_messages" in state_to_save:
        state_to_save["motivator_messages"] = serialize_messages(state_to_save["motivator_messages"])
    
    with open(SHARED_MEMORY_FILE, "w") as f:
        json.dump(state_to_save, f, indent=2)

def getassignments():
    memory = load_shared_memory()
    return memory.get("assignments", [])

def add_assignment(assignment):
    memory = load_shared_memory()
    memory["assignments"].append(assignment)
    save_shared_memory(memory)
