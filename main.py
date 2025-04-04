from flask import Flask, request
import telebot
import time
from telebot import types
from start import setup_start_handler
from verify import setup_verification_handler
from menu import show_main_menu
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "YOUR_BOT_TOKEN"
WEBHOOK_URL = f"https://nine77105-rosy.onrender.com/{BOT_TOKEN}"  # ✅ Update if your URL is different

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ✅ Dummy user database (you should replace with actual storage)
users = {}
user_modes = {}

# ✅ Setup all handlers
setup_start_handler(bot, users, user_modes)
setup_verification_handler(bot, users)

# ✅ Fallback handler for testing
@bot.message_handler(func=lambda msg: True)
def fallback(msg):
    print(f"📩 Message from {msg.chat.id}: {msg.text}")
    bot.send_message(msg.chat.id, "🤖 I'm alive, but unrecognized command!")

# ✅ Webhook route to process updates
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.get_data().decode("utf-8")
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

# ✅ Default homepage route
@app.route("/", methods=["GET"])
def index():
    return "👾 H4CKUCATOR Bot is Live", 200

# ✅ Main app start
if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL)
    print("🚀 Webhook set. Bot is live!")

    app.run(host="0.0.0.0", port=10000)

