import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "escalations.json")

def create_escalation(ticket_id, reason):

    data = []

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            data = json.load(f)

    record = {
        "ticket_id": ticket_id,
        "reason": reason,
        "status": "OPEN"
    }

    data.append(record)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

    return record