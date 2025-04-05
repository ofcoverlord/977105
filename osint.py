import requests
from telebot import types
from datetime import datetime

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

            # 🔎 Extract fields
            name = data.get("Truecaller") or "No name found"
            unknown = data.get("Unknown", "N/A")
            carrier = data.get("carrier", "N/A")
            location = data.get("location", "N/A")
            country = data.get("country", "N/A")
            intl_format = data.get("international_format", "N/A")
            local_format = data.get("local_format", "N/A")
            is_possible = "✅ Yes" if data.get("is_possible") else "❌ No"
            timezones = ", ".join(data.get("timezones", [])) if isinstance(data.get("timezones"), list) else "N/A"
            timestamp = data.get("timestamp")
            photo = data.get("photo")

            formatted_time = "N/A"
            if timestamp:
                try:
                    dt = datetime.fromtimestamp(timestamp / 1000)
                    formatted_time = dt.strftime("%d %B %Y, %I:%M %p")
                except:
                    pass

            # 🧠 Build reply
            reply = f"""📞 *Name:* {name}
🧑‍🦰 *Alt Name:* {unknown}
📡 *Carrier:* {carrier}
🌍 *Location:* {location}
🌎 *Country:* {country}
⏰ *Timezone:* {timezones}
📲 *Intl Format:* {intl_format}
📱 *Local Format:* {local_format}
📶 *Is Valid Number:* {is_possible}
🕒 *Last Updated:* {formatted_time}"""

            # 🖼️ With profile image
            if photo:
                bot.send_photo(message.chat.id, photo, caption=reply, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, reply, parse_mode="Markdown")

        except Exception as e:
            print("OSINT Error:", e)
            bot.send_message(message.chat.id, "⚠️ Could not fetch data. Please try again later.")

    # Optional: exit OSINT mode if another button is clicked
    @bot.message_handler(func=lambda msg: user_modes.get(msg.chat.id) == "osint" and msg.text not in ["🕵️ OSINT Tools"])
    def deactivate_osint_mode(msg):
        user_modes[msg.chat.id] = None

