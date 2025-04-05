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

            name = data.get("name", "N/A")
            alt_name = data.get("alt_name", "N/A")
            email = data.get("email", "N/A")
            carrier = data.get("carrier", "N/A")
            city = data.get("city", "N/A")
            country = data.get("country", "N/A")
            time_zone = data.get("time_zone", "N/A")
            job = data.get("job", "N/A")
            gender = data.get("gender", "N/A")
            internet_addresses = ", ".join(data.get("internet_addresses", [])) or "N/A"
            organization = data.get("organization", "N/A")
            photo = data.get("photo", None)

            reply = (
                f"📞 *Name:* {name}\n"
                f"🧑‍🦰 *Alt Name:* {alt_name}\n"
                f"✉️ *Email:* {email}\n"
                f"🏢 *Organization:* {organization}\n"
                f"👤 *Job:* {job}\n"
                f"🌐 *Internet Profiles:* {internet_addresses}\n"
                f"📡 *Carrier:* {carrier}\n"
                f"🌍 *Location:* {city}, {country}\n"
                f"⏰ *Timezone:* {time_zone}\n"
                f"⚧ *Gender:* {gender}"
            )

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


