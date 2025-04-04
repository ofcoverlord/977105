import json
import os

DATA_FILE = "users.json"

def load_users():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_user(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

def init_db():
    """Ensure the user database file exists and return loaded user data"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
    
    return load_users()  # ✅ Return user data
