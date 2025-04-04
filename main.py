import os
from flask import Flask, request
from telebot import TeleBot, types

# Your Bot Token and Webhook URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)
WEBHOOK_URL = f"https://your-app-name.onrender.com/{BOT_TOKEN}"  # Replace with your Render URL

# Import all handlers and DB
from handlers.start import setup_start_handler
from handlers.admin import setup_admin_handlers
from handlers.verify import setup_verification_handler
from handlers.phishing import setup_phishing_handler
from handlers.osint import setup_osint_handler
from handlers.camera import setup_camera_handler
from handlers.location import setup_location_handler
from handlers.broadcast import setup_broadcast_handler
from utils.database import init_db

# Flask App
app = Flask(__name__)

# Database and user mode setup
db = init_db()
user_modes = {}  # Replace with actual logic

# Setup Handlers
setup_start_handler(bot, db, user_modes)
setup_verification_handler(bot, db)
setup_phishing_handler(bot)
setup_osint_handler(bot, user_modes)
setup_camera_handler(bot)
setup_admin_handlers(bot)
setup_location_handler(bot)
setup_broadcast_handler(bot, db, admin_id=7407431042)

# Webhook route
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# Root test route
@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot is running on Render with Webhook!"

# Set webhook and start Flask
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🚀 Webhook set. Bot is live!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

