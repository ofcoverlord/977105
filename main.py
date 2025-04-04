from flask import Flask, request
import telebot
import time
import os
from telebot import types
from start import setup_start_handler
from verify import setup_verification_handler
from menu import show_main_menu, setup_menu_handler  # ✅ Import added

# 🔐 Load your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
WEBHOOK_URL = f"https://nine77105-rosy.onrender.com/{BOT_TOKEN}"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Dummy DB
users = {}
user_modes = {}

# ✅ Setup Handlers
print("⚙️ Registering command handlers...")
setup_start_handler(bot, users, user_modes)
setup_verification_handler(bot, users)
setup_menu_handler(bot)  # ✅ Register menu buttons
print("✅ All handlers ready!")

# Fallback for unknown text (not commands or buttons)
@bot.message_handler(func=lambda msg: not msg.text.startswith("/"))
def fallback(msg):
    print(f"📩 Fallback message: {msg.text}")
    bot.send_message(msg.chat.id, "🤖 I'm alive, but unrecognized command!")

# Webhook endpoint
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_str = request.get_data().decode("utf-8")
        update = types.Update.de_json(json_str)
        print(f"🔗 Webhook update received.")
        bot.process_new_updates([update])
        return "OK", 200
    return "Forbidden", 403

# Health check
@app.route("/", methods=["GET"])
def index():
    return "👾 H4CKUCATOR Bot is Live", 200

@app.route("/webhook_status", methods=["GET"])
def webhook_status():
    import requests
    response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo")
    return response.json(), 200

# Startup
if __name__ == "__main__":
    print("⚙️ Removing old webhook...")
    bot.remove_webhook()
    time.sleep(1)
    print(f"🚀 Setting new webhook: {WEBHOOK_URL}")
    success = bot.set_webhook(url=WEBHOOK_URL)
    if success:
        print("✅ Webhook set! Bot is live.")
    else:
        print("❌ Failed to set webhook.")
    app.run(host="0.0.0.0", port=10000)


