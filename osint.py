from telebot import types
import requests
import re

def setup_osint_handler(bot, user_modes):

    def is_valid_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_valid_phone(number):
        return re.match(r"^\+?[0-9]{10,13}$", number)

    def is_valid_username(username):
        return re.match(r"^[a-zA-Z0-9_.]{3,30}$", username)

    @bot.message_handler(commands=["osint"])
    def osint_menu(msg):
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb.add(
            types.InlineKeyboardButton("📸 Instagram", callback_data="osint_instagram"),
            types.InlineKeyboardButton("📱 Free Fire", callback_data="osint_ff"),
            types.InlineKeyboardButton("📘 Facebook", callback_data="osint_fb"),
            types.InlineKeyboardButton("🎮 BGMI", callback_data="osint_bgmi"),
            types.InlineKeyboardButton("👻 Snapchat", callback_data="osint_snap"),
            types.InlineKeyboardButton("🎵 Spotify", callback_data="osint_spotify"),
            types.InlineKeyboardButton("📧 Gmail", callback_data="osint_gmail")
        )
        bot.send_message(msg.chat.id, "⚠️ *For ethical hacking learning only. Don't misuse.*", parse_mode="Markdown", reply_markup=kb)

        msg_text = (
            "🧠 *OSINT MODE ON*\n\n"
            "Send:\n"
            "✉️ Email • 📱 Number • 👤 Username\n"
        )
        bot.send_message(msg.chat.id, msg_text, parse_mode="Markdown")

    @bot.callback_query_handler(func=lambda call: call.data.startswith("osint_"))
    def handle_buttons(call):
        bot.answer_callback_query(call.id, "🧠 Enter detail below to scan...")
    
    @bot.message_handler(func=lambda m: True)
    def handle_osint_queries(msg):
        text = msg.text.strip()

        if is_valid_phone(text):
            send_phone_details(bot, msg.chat.id, text)
        elif is_valid_email(text):
            send_email_leak(bot, msg.chat.id, text)
        elif is_valid_username(text):
            send_instagram_info(bot, msg.chat.id, text)
        else:
            bot.send_message(msg.chat.id, "❌ Invalid format. Please send a valid phone, email, or username.")

    def send_phone_details(bot, chat_id, number):
        if not number.startswith("+"):
            number = "+91" + number
        
        api_url = f"https://truecaller.privates-bots.workers.dev/?q={number}"
        res = requests.get(api_url).json()

        if res.get("name"):
            msg = f"📱 *Truecaller Info for {number}*\n\n"
            msg += f"👤 Name: `{res.get('name')}`\n"
            msg += f"📍 Location: `{res.get('city', 'N/A')}, {res.get('country', '')}`\n"
            msg += f"📞 Carrier: `{res.get('carrier', 'N/A')}`\n"
            msg += f"🆔 Type: `{res.get('type', 'N/A')}`\n"
            msg += "\n✅ Powered by H4CKUCATOR"
        else:
            msg = "❌ No data found for this number."

        bot.send_message(chat_id, msg, parse_mode="Markdown")

    def send_instagram_info(bot, chat_id, username):
        url = f"https://instainfo.rishuapi.workers.dev/info?username={username}"
        res = requests.get(url).json()

        if res.get("username"):
            full_name = res.get("full_name", "")
            bio = res.get("biography", "No bio.")
            followers = res.get("followers", "N/A")
            following = res.get("following", "N/A")
            is_private = res.get("is_private", False)
            profile_pic = res.get("profile_pic_url_hd")

            text = f"📸 *Instagram Info: @{username}*\n\n"
            text += f"👤 Name: `{full_name}`\n"
            text += f"🔐 Private: `{is_private}`\n"
            text += f"📍 Followers: `{followers}`\n"
            text += f"👥 Following: `{following}`\n"
            text += f"📝 Bio:\n`{bio}`"

            buttons = types.InlineKeyboardMarkup()
            buttons.add(
                types.InlineKeyboardButton("📚 Posts", url=f"https://instainfo.rishuapi.workers.dev/posts?username={username}"),
                types.InlineKeyboardButton("📖 Stories", url=f"https://instainfo.rishuapi.workers.dev/stories?username={username}"),
                types.InlineKeyboardButton("🎬 Reels", url=f"https://instainfo.rishuapi.workers.dev/reels?username={username}"),
                types.InlineKeyboardButton("📂 Highlights", url=f"https://instainfo.rishuapi.workers.dev/highlights?username={username}")
            )

            bot.send_photo(chat_id, profile_pic, caption=text, parse_mode="Markdown", reply_markup=buttons)
        else:
            bot.send_message(chat_id, "⚠️ Instagram lookup failed. Try again later.")

    def send_email_leak(bot, chat_id, email):
        msg = f"🕵️ Email leak check for `{email}`\n\n"
        msg += "🔍 Scanning dark web databases...\n"
        msg += "⚠️ Feature under construction."
        bot.send_message(chat_id, msg, parse_mode="Markdown")

