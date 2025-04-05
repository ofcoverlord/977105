import re
import requests
from telebot import types
from user_db import (
    can_use_osint,
    add_osint_usage,
    get_referral_link,
    is_admin,
    get_remaining_uses,
    add_referral
)

# Your two verification channel IDs
CHANNEL_1 = -1002470294091
CHANNEL_2 = -1002340797968

# Sherlock API for username scan
SHERLOCK_API = "https://sherlock.rishuapi.workers.dev/?username="

def setup_osint_handler(bot, user_modes):

    @bot.message_handler(func=lambda msg: msg.text == "🕵️ OSINT Tools")
    def show_osint_guide(msg):
        chat_id = msg.chat.id
        user_modes[chat_id] = "osint"
        remaining = get_remaining_uses(msg.from_user.id)
        bot.send_message(chat_id,
            f"🧠 *OSINT MODE ON*\n\n"
            f"Send:\n"
            f"📧 Email  •  📱 Number  •  👤 Username\n\n"
            f"🪪 *Remaining Scans:* `{remaining}`\n"
            f"_Refer friends to earn more!_ 🎁",
            parse_mode="Markdown")

    @bot.message_handler(func=lambda msg: user_modes.get(msg.chat.id) == "osint", content_types=["text"])
    def handle_osint(msg):
        chat_id = msg.chat.id
        user_id = str(msg.from_user.id)
        text = msg.text.strip()

        if not is_admin(user_id) and not can_use_osint(user_id):
            link = get_referral_link(user_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🎁 Refer to Unlock Scans", url=link))
            bot.send_message(chat_id,
                "⚠️ *Limit Reached!*\n\nInvite friends to earn more scans.\nEach friend = 1 scan (they must join 2 channels).",
                parse_mode="Markdown", reply_markup=markup)
            return

        # ✅ Detect what was sent
        if is_email(text):
            lookup_email(bot, chat_id, text)
        elif is_phone(text):
            lookup_phone(bot, chat_id, text)
        elif is_username(text):
            lookup_username(bot, chat_id, text)
        else:
            bot.send_message(chat_id, "❌ Invalid format.\nSend email, phone, or username.")
            return

        if not is_admin(user_id):
            add_osint_usage(user_id)

# 🧠 Input Validators
def is_email(data): return re.match(r"[^@]+@[^@]+\.[^@]+", data)
def is_phone(data): return re.match(r"^\+?\d{7,15}$", data)
def is_username(data): return re.match(r"^[a-zA-Z0-9_.]{3,30}$", data)

# ✅ Email Leak Lookup
def lookup_email(bot, chat_id, email):
    bot.send_chat_action(chat_id, 'typing')
    try:
        res = requests.get(f"https://haveibeenpwned.com/unifiedsearch/{email}", headers={"User-Agent": "OSINT-Bot"})
        if "BreachName" in res.text:
            bot.send_message(chat_id,
                f"🛑 *Email Breached!*\n\n"
                f"🔎 `{email}` found in known data breaches.\n"
                f"🔗 https://haveibeenpwned.com/account/{email}",
                parse_mode="Markdown")
        else:
            bot.send_message(chat_id, f"✅ `{email}` is safe! No leaks found.", parse_mode="Markdown")
    except:
        bot.send_message(chat_id, "⚠️ Error checking email. Try later.")

# ✅ Phone Lookup (Truecaller + WhatsApp)
def lookup_phone(bot, chat_id, number):
    bot.send_chat_action(chat_id, 'typing')
    try:
        res = requests.get(f"https://newtrue.rishuapi.workers.dev/?number={number}").json()

        if res.get("name"):
            info = (
                f"📱 *Phone Info:*\n\n"
                f"👤 *Name:* `{res.get('name')}`\n"
                f"📍 *Location:* {res.get('city')}, {res.get('country')}\n"
                f"🏢 *Carrier:* {res.get('carrier')}\n"
                f"🔗 *WhatsApp:* [Chat Now](https://wa.me/{number.replace('+','')})"
            )
            bot.send_message(chat_id, info, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(chat_id, "❌ No data found for this number.")
    except:
        bot.send_message(chat_id, "⚠️ Error fetching number info. Try later.")

# ✅ Username Lookup (Sherlock + Instagram)
def lookup_username(bot, chat_id, username):
    bot.send_chat_action(chat_id, 'typing')

    # 1. Check Instagram first
    try:
        res = requests.get(f"https://instainfo.rishuapi.workers.dev/info?username={username}", timeout=4)
        data = res.json()

        if data.get("status") == "ok":
            profile = data["data"]
            caption = (
                f"📸 *Instagram Info:*\n\n"
                f"🧿 `{profile.get('username')}`\n"
                f"👤 {profile.get('full_name')}\n"
                f"📷 Posts: {profile.get('media_count')} | 👥 {profile.get('follower_count')} followers\n"
                f"🔗 https://instagram.com/{profile.get('username')}"
            )
            if profile.get("profile_pic_url_hd"):
                bot.send_photo(chat_id, profile["profile_pic_url_hd"], caption=caption, parse_mode="Markdown")
            else:
                bot.send_message(chat_id, caption, parse_mode="Markdown")
    except:
        pass  # Proceed to sherlock anyway

    # 2. Check with Sherlock API
    try:
        sherlock = requests.get(SHERLOCK_API + username).json()
        if "results" in sherlock:
            results = sherlock["results"]
            text = "🌐 *Username Found On:*\n\n"
            for platform, url in results.items():
                text += f"🔹 *{platform.title()}*: [View Profile]({url})\n"
            bot.send_message(chat_id, text, parse_mode="Markdown", disable_web_page_preview=True)
        else:
            bot.send_message(chat_id, "❌ Username not found on any major platform.")
    except:
        bot.send_message(chat_id, "⚠️ Sherlock lookup failed. Try later.")

# ✅ Referral Validator (to be used in your /start handler)
def verify_user_joined(bot, user_id):
    try:
        status1 = bot.get_chat_member(CHANNEL_1, user_id).status
        status2 = bot.get_chat_member(CHANNEL_2, user_id).status
        return status1 in ["member", "administrator", "creator"] and status2 in ["member", "administrator", "creator"]
    except:
        return False

def handle_referral(bot, msg):
    if msg.text and msg.text.startswith("/start "):
        inviter_id = msg.text.split(" ")[1]
        if verify_user_joined(bot, msg.from_user.id):
            add_referral(inviter_id, msg.from_user.id)

