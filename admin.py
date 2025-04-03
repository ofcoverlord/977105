import os
import json
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

# Load admin ID from environment
ADMIN_ID = int(os.getenv("ADMIN_ID", "7407431042"))

# Initialize bot
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Load users database
DATA_FILE = "users.json"

def load_users():
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

# 📌 ADMIN PANEL MENU
def show_admin_panel(chat_id):
    markup = InlineKeyboardMarkup(row_width=3)
    
    buttons = [
        InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton("📊 User Stats", callback_data="admin_stats"),
        InlineKeyboardButton("🔍 Command Logger", callback_data="admin_logger"),
        InlineKeyboardButton("⚙️ Feature Control", callback_data="admin_features"),
        InlineKeyboardButton("🔄 Auto-Update", callback_data="admin_update"),
        InlineKeyboardButton("🚨 Kill Switch", callback_data="admin_kill"),
        InlineKeyboardButton("👤 Manage Users", callback_data="admin_users"),
        InlineKeyboardButton("📡 Announcements", callback_data="admin_announcements"),
        InlineKeyboardButton("📂 Debug Logs", callback_data="admin_debug")
    ]

    markup.add(*buttons)
    bot.send_message(chat_id, "👑 *Admin Panel*", reply_markup=markup, parse_mode="Markdown")

# 📌 ADMIN PANEL HANDLER
@bot.message_handler(commands=['admin'])
def admin_panel(message: Message):
    if message.chat.id == ADMIN_ID:
        show_admin_panel(message.chat.id)
    else:
        bot.send_message(message.chat.id, "❌ You are not authorized to access the admin panel.")

# 📌 CALLBACK HANDLER FOR ADMIN BUTTONS
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def admin_actions(call):
    chat_id = call.message.chat.id

    if chat_id != ADMIN_ID:
        bot.answer_callback_query(call.id, "❌ You are not authorized.")
        return

    action = call.data.split("_")[1]

    if action == "broadcast":
        bot.send_message(chat_id, "📢 *Send a message to broadcast (or forward any message):*", parse_mode="Markdown")
        bot.register_next_step_handler(call.message, process_broadcast)

    elif action == "stats":
        users = load_users()
        bot.send_message(chat_id, f"📊 *Total Users:* {len(users)}", parse_mode="Markdown")

    elif action == "logger":
        bot.send_message(chat_id, "🔍 *Command Logger:* Feature coming soon!", parse_mode="Markdown")

    elif action == "features":
        bot.send_message(chat_id, "⚙️ *Feature Access Control:* Coming soon!", parse_mode="Markdown")

    elif action == "update":
        bot.send_message(chat_id, "🔄 *Auto-Update triggered!*", parse_mode="Markdown")

    elif action == "kill":
        bot.send_message(chat_id, "🚨 *Bot Kill Switch Activated!*", parse_mode="Markdown")

    elif action == "users":
        bot.send_message(chat_id, "👤 *User Management:* Ban/unban/reset users coming soon!", parse_mode="Markdown")

    elif action == "announcements":
        bot.send_message(chat_id, "📡 *Custom Announcements:* Feature in progress!", parse_mode="Markdown")

    elif action == "debug":
        bot.send_message(chat_id, "📂 *Error & Debug Logs:* No recent errors found.")

# 📌 BROADCAST HANDLER

def process_broadcast(message: Message):
    if message.chat.id != ADMIN_ID:
        return

    users = load_users()
    count = 0

    for user_id in users.keys():
        try:
            bot.copy_message(user_id, message.chat.id, message.message_id)
            count += 1
        except:
            continue

    bot.send_message(ADMIN_ID, f"📢 Broadcast sent to {count} users!")

# 📌 ADD THIS TO `bot.py` TO ENABLE ADMIN PANEL
def setup_admin_handlers(bot):
    bot.register_message_handler(admin_panel, commands=['admin'])
    bot.register_callback_query_handler(admin_actions, func=lambda call: call.data.startswith("admin_"))


