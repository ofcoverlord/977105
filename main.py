import os
from flask import Flask, request
from telebot import TeleBot, types

# Bot token and webhook URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)
WEBHOOK_URL = f"https://977105.onrender.com/{BOT_TOKEN}"  # Replace with your Render URL

# Import handlers (now in flat structure)
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

# Initialize DB and user modes
db = init_db()
user_modes = {}  # Replace with actual logic

# Register handlers
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

# Root route
@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot is running on Render with Webhook!"

# Set webhook and start server
if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print("🚀 Webhook set. Bot is live!")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


