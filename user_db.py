import json
import os

USERS_FILE = "users.json"
REFERRALS_FILE = "referrals.json"

def load_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def is_admin(user_id):
    return str(user_id) == "7407431042"  # ✅ Your admin ID

# ✅ Check if user can use OSINT
def can_use_osint(user_id):
    data = load_json(USERS_FILE)
    user = data.get(str(user_id), {"uses": 0, "bonus": 0})
    total_allowed = 1 + user.get("bonus", 0)
    return user.get("uses", 0) < total_allowed

# ✅ Add OSINT usage
def add_osint_usage(user_id):
    user_id = str(user_id)
    data = load_json(USERS_FILE)
    if user_id not in data:
        data[user_id] = {"uses": 1, "bonus": 0}
    else:
        data[user_id]["uses"] = data[user_id].get("uses", 0) + 1
    save_json(USERS_FILE, data)

# ✅ Referral link generator
def get_referral_link(user_id):
    return f"https://t.me/VERIFICATIONNARUTO?start={user_id}"

# ✅ Count referral for inviter
def add_referral(inviter_id, new_user_id):
    inviter_id = str(inviter_id)
    new_user_id = str(new_user_id)
    if inviter_id == new_user_id:
        return

    ref_data = load_json(REFERRALS_FILE)
    users_data = load_json(USERS_FILE)

    if inviter_id not in ref_data:
        ref_data[inviter_id] = []

    if new_user_id in ref_data[inviter_id]:
        return  # already referred

    ref_data[inviter_id].append(new_user_id)

    # Grant 1 bonus OSINT use for every 3 invites
    total_refs = len(ref_data[inviter_id])
    bonus = total_refs // 3

    if inviter_id not in users_data:
        users_data[inviter_id] = {"uses": 0, "bonus": bonus}
    else:
        users_data[inviter_id]["bonus"] = bonus

    save_json(REFERRALS_FILE, ref_data)
    save_json(USERS_FILE, users_data)

# ✅ Remaining uses
def get_remaining_uses(user_id):
    data = load_json(USERS_FILE)
    user = data.get(str(user_id), {"uses": 0, "bonus": 0})
    allowed = 1 + user.get("bonus", 0)
    return allowed - user.get("uses", 0)

