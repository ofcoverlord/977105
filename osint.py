from telebot.types import Message
import requests
from telebot import TeleBot

# 🧠 Temporary state to track active OSINT session
user_osint_mode = {}

def setup_osint_handler(bot: TeleBot, user_modes):

    @bot.message_handler(func=lambda message: message.text == "🕵️ OSINT Tools")
    def activate_osint_mode(message: Message):
        user_osint_mode[message.from_user.id] = True
        bot.send_message(
            message.chat.id,
            "🕵️ *OSINT Mode Activated!*\n\nSend me a phone number like `+919876543210` 📞 and I’ll search Truecaller for details.",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda msg: user_osint_mode.get(msg.from_user.id) is True)
    def handle_osint_query(message: Message):
        user_id = message.from_user.id
        number = message.text.strip()

        if not number.startswith("+"):
            bot.send_message(message.chat.id, "⚠️ Please enter number with country code like +91...")
            return

        bot.send_message(message.chat.id, f"🔍 Searching for `{number}` on Truecaller...", parse_mode="Markdown")

        try:
            url = f"https://truecaller.privates-bots.workers.dev/?q={number}"
            response = requests.get(url)
            data = response.json()

            if data.get("name"):
                name = data.get("name", "N/A")
                carrier = data.get("carrier", "N/A")
                location = data.get("location", "N/A")

                bot.send_message(
                    message.chat.id,
                    f"📞 *Name:* {name}\n📡 *Carrier:* {carrier}\n📍 *Location:* {location}",
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(message.chat.id, "❌ No details found for this number.")

        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ API Error: `{str(e)}`", parse_mode="Markdown")

        # 🔻 Deactivate OSINT mode after lookup
        user_osint_mode[user_id] = False

    # 🔻 Deactivate OSINT if user taps anything else
    @bot.message_handler(func=lambda msg: msg.text != "🕵️ OSINT Tools" and user_osint_mode.get(msg.from_user.id))
    def deactivate_osint_mode(message: Message):
        user_osint_mode[message.from_user.id] = False

