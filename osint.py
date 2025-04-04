import re
import requests
from telebot import types
from bs4 import BeautifulSoup
from user_db import can_use_osint, add_osint_usage, get_referral_link, is_admin

TRUECALLER_API_KEY = "ee74f88abcmshe019247b16f750bp1d4f84jsn6e959aafb711"

def setup_osint_handler(bot, user_modes):  # <- user_modes passed from main.py

    @bot.message_handler(func=lambda msg: msg.text == "🕵️ OSINT Tools")
    def show_instruction(msg):
        chat_id = msg.chat.id
        user_modes[chat_id] = "osint"
        bot.send_message(chat_id,
            "🕵️ *OSINT TOOL GUIDE*\n\n"
            "Send one of the following:\n"
            "📧 Email\n📱 Phone Number\n👤 Username\n\n"
            "_Real-time public data only._",
            parse_mode="Markdown")

    @bot.message_handler(func=lambda msg: user_modes.get(msg.chat.id) == "osint", content_types=["text"])
    def handle_osint(msg):
        chat_id = msg.chat.id
        user_id = str(msg.from_user.id)
        text = msg.text.strip()

        if text in ["🌐 Dark Web Search", "🕵️ OSINT Tools"]:
            return

        if not is_admin(user_id) and not can_use_osint(user_id):
            link = get_referral_link(user_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔗 Refer to Unlock", url=link))
            bot.send_message(chat_id,
                "⚠️ *You've reached your OSINT limit.*\n\nInvite 3 friends to unlock more.",
                parse_mode="Markdown", reply_markup=markup)
            return

        if is_email(text):
            lookup_email(bot, chat_id, text)
        elif is_phone(text):
            lookup_phone(bot, chat_id, text)
        elif is_username(text):
            lookup_username(bot, chat_id, text)
        else:
            bot.send_message(chat_id, "❌ Invalid input.\nSend a valid email, phone number, or username.")
            return

        if not is_admin(user_id):
            add_osint_usage(user_id)

# 🧠 Validators
def is_email(data): return re.match(r"[^@]+@[^@]+\.[^@]+", data)
def is_phone(data): return re.match(r"^\+?\d{7,15}$", data)
def is_username(data): return re.match(r"^[a-zA-Z0-9_.]{3,30}$", data)

# 📧 Email Lookup
def lookup_email(bot, chat_id, email):
    bot.send_chat_action(chat_id, 'typing')
    try:
        res = requests.get(f"https://haveibeenpwned.com/unifiedsearch/{email}", headers={"User-Agent": "OSINT-Bot"})
        if "BreachName" in res.text:
            bot.send_message(chat_id, f"🛑 *Email Breached!*\n\n🔎 `{email}` was found in leaks.\nCheck: https://haveibeenpwned.com/account/{email}", parse_mode="Markdown")
        else:
            bot.send_message(chat_id, f"✅ `{email}` is not found in any known breaches.", parse_mode="Markdown")
    except:
        bot.send_message(chat_id, "⚠️ Email lookup failed.")

# 📱 Phone Lookup
def lookup_phone(bot, chat_id, number):
    bot.send_chat_action(chat_id, 'typing')
    try:
        headers = {
            "X-RapidAPI-Key": TRUECALLER_API_KEY,
            "X-RapidAPI-Host": "truecallr.p.rapidapi.com"
        }
        res = requests.get(f"https://truecallr.p.rapidapi.com/trace/{number}", headers=headers).json()
        if res.get("name"):
            info = (
                f"📞 *Phone Lookup:*\n\n"
                f"👤 Name: `{res.get('name')}`\n"
                f"🌍 Location: {res.get('location')}\n"
                f"📱 Carrier: {res.get('carrier')}\n"
                f"🔒 Type: {res.get('type')}"
            )
            bot.send_message(chat_id, info, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, "❌ No info found for this number.")
    except:
        bot.send_message(chat_id, "⚠️ Error during phone lookup.")

# 👤 Username Lookup
def lookup_username(bot, chat_id, username):
    bot.send_chat_action(chat_id, 'typing')
    platforms = {
        "Instagram": f"https://www.instagram.com/{username}/",
        "Telegram": f"https://t.me/{username}",
        "Twitter": f"https://twitter.com/{username}"
    }

    found = False
    for platform, url in platforms.items():
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                image_url = extract_profile_image(res.text)
                if image_url:
                    bot.send_photo(chat_id, image_url, caption=f"👤 {platform} Profile\n🔗 {url}")
                else:
                    bot.send_message(chat_id, f"👤 {platform} Profile\n🔗 {url}")
                found = True
        except:
            continue

    if not found:
        bot.send_message(chat_id, "❌ Username not found on major platforms.")

def extract_profile_image(html):
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find("meta", property="og:image")
    return tag['content'] if tag and 'content' in tag.attrs else None
