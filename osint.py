
import requests
from telebot import types

def setup_osint_handler(bot, user_modes):

    @bot.message_handler(func=lambda message: message.text == "🕵️ OSINT Tools")
    def activate_osint_mode(message):
        user_id = message.chat.id
        user_modes[user_id] = "osint"
        bot.send_message(
            user_id,
            "🕵️ OSINT Mode Activated!\n\nSend me a phone number like +919876543210 📞 and I’ll search Truecaller for full details."
        )

    @bot.message_handler(func=lambda message: user_modes.get(message.chat.id) == "osint")
    def handle_osint_lookup(message):
        number = message.text.strip()

        if not number.startswith("+"):
            bot.send_message(message.chat.id, "⚠️ Please enter a valid number with +countrycode, e.g. +91xxxxxxxxxx")
            return

        bot.send_message(message.chat.id, f"🔍 Searching for {number} on Truecaller...")

        try:
            url = f"https://truecaller.privates-bots.workers.dev/?q={number}"
            res = requests.get(url)
            data = res.json()

            # 🧠 Smart extraction
            name = data.get("Truecaller") or data.get("Unknown") or "N/A"
            carrier = data.get("carrier", "N/A")
            location = data.get("location", "N/A")
            country = data.get("country", "N/A")
            international_format = data.get("international_format", "N/A")
            local_format = data.get("local_format", "N/A")
            timezones = ", ".join(data.get("timezones", [])) if isinstance(data.get("timezones"), list) else data.get("timezones", "N/A")
            photo = data.get("photo", None)

            # 🔎 Clean Reply Builder
            reply_parts = []

            if name and name != "N/A":
                reply_parts.append(f"📞 *Name:* {name}")
            if carrier and carrier != "N/A":
                reply_parts.append(f"📡 *Carrier:* {carrier}")
            if location and location != "N/A":
                reply_parts.append(f"🌍 *Location:* {location}")
            if country and country != "N/A":
                reply_parts.append(f"🌎 *Country:* {country}")
            if timezones and timezones != "N/A":
                reply_parts.append(f"⏰ *Timezone:* {timezones}")
            if international_format and international_format != "N/A":
                reply_parts.append(f"📲 *Intl Format:* {international_format}")
            if local_format and local_format != "N/A":
                reply_parts.append(f"📱 *Local Format:* {local_format}")

            if not reply_parts:
                reply_parts.append("⚠️ No useful data found for this number.")

            reply = "\n".join(reply_parts)

            # 🖼️ Send with image if available
            if photo:
                bot.send_photo(message.chat.id, photo, caption=reply, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, reply, parse_mode="Markdown")

        except Exception as e:
            print("OSINT Error:", e)
            bot.send_message(message.chat.id, "⚠️ Could not fetch data. Please try again later.")

    @bot.message_handler(func=lambda message: user_modes.get(message.chat.id) == "osint" and message.text != "🕵️ OSINT Tools")
    def deactivate_osint_mode(message):
        user_modes[message.chat.id] = None

