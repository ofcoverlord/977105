import os
from flask import Flask, request
from telebot import TeleBot, types

# ✅ Load Bot Token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN not found in environment variables")

# ✅ Create bot and Flask app
bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ✅ Webhook URL (update with your Render subdomain)
WEBHOOK_URL = f"https://977105.onrender.com/{BOT_TOKEN}"

# ✅ Import handlers
from start import setup_start_handler
from admin import setup_admin_handlers
from verify import setup_verification_handler
from phishing import setup_phishing_handler
from osint import setup_osint_handler
from camera import setup_camera_handler
from location import setup_location_handler
from broadcast import setup_broadcast_handler
from database import init_db

# ✅ Initialize DB and user state
db = init_db()
user_modes = {}

# ✅ Register handlers
setup_start_handler(bot, db, user_modes)
setup_verification_handler(bot, db)
setup_phishing_handler(bot)
setup_osint_handler(bot, user_modes)
setup_camera_handler(bot)
setup_admin_handlers(bot)
setup_location_handler(bot)
setup_broadcast_handler(bot, db, admin_id=7407431042)

# ✅ Webhook route (important!)
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_data().decode("utf-8")
    update = types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# ✅ Root route (for test browser access)
@app.route("/", methods=["GET"])
def home():
    return "🚀 Bot is running on Render with Webhook!"

# ✅ Start everything
if __name__ == "__main__":
    print("⚙️ Removing old webhook...")
    bot.remove_webhook()

    print("🚀 Setting new webhook...")
    bot.set_webhook(url=WEBHOOK_URL)

    print("✅ Webhook set. Bot is live!")

    # Start Flask server
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


