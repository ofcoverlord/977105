import requests
from telebot import types

def setup_osint_handler(bot, user_modes):

    @bot.message_handler(func=lambda message: message.text == "🕵️ OSINT Tools")
    def activate_osint_mode(message):
        user_id = message.chat.id
        user_modes[user_id] = "osint"
        bot.send_message(
            user_id,
            "🕵️ *OSINT Mode Activated!*\n\nSend me a phone number like `+919876543210` 📞 and I’ll search Truecaller for details.",
            parse_mode="Markdown"
        )

    @bot.message_handler(func=lambda message: user_modes.get(message.chat.id) == "osint")
    def handle_phone_number(message):
        number = message.text.strip()
        if not number.startswith("+"):
            bot.send_message(message.chat.id, "⚠️ Please send a valid phone number with country code, like `+91xxxxxxxxxx`.", parse_mode="Markdown")
            return

        bot.send_message(message.chat.id, f"🔍 Searching for `{number}` on Truecaller...", parse_mode="Markdown")

        try:
            url = f"https://truecaller.privates-bots.workers.dev/?q={number}"
            response = requests.get(url)
            data = response.json()

            name = data.get("name", "N/A")
            carrier = data.get("carrier", "N/A")
            location = data.get("location", "N/A")

            if name == "N/A" and carrier == "N/A" and location == "N/A":
                bot.send_message(message.chat.id, "❌ No details found for this number.")
            else:
                bot.send_message(
                    message.chat.id,
                    f"📞 *Name:* {name}\n📡 *Carrier:* {carrier}\n📍 *Location:* {location}",
                    parse_mode="Markdown"
                )

        except Exception as e:
            print(f"OSINT error: {e}")
            bot.send_message(message.chat.id, "⚠️ An error occurred while fetching the data. Please try again later.")

    @bot.message_handler(func=lambda message: user_modes.get(message.chat.id) == "osint" and message.text != "🕵️ OSINT Tools")
    def deactivate_on_other_buttons(message):
        if message.text not in ["🕵️ OSINT Tools"]:
            user_modes[message.chat.id] = None

