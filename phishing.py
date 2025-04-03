from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot
from handlers.start import show_main_menu

PHISHING_IMAGE_URL = "https://ibb.co/0jH3KL5s"  # Replace with your phishing image URL

# Dictionary of phishing pages
PHISHING_DATA = {
    "instagram": {
        "name": "Instagram",
        "emoji": "📸",
        "caption": "This page looks like the real Instagram login. You can use it to educate people about how phishing works. Send this link to a friend and show them how easy it is to get tricked.\n\nThis is for ethical awareness only. Never use it for illegal activity.",
        "link": "https://example.com/phish/instagram"
    },
    "freefire": {
        "name": "Free Fire",
        "emoji": "🔥",
        "caption": "This phishing demo mimics the Free Fire rewards site. Use it to spread awareness about gaming scams. Show friends how fake pages steal login info.\n\n⚠️ For cybersecurity learning only.",
        "link": "https://example.com/phish/freefire"
    },
    "facebook": {
        "name": "Facebook",
        "emoji": "📘",
        "caption": "This page is a Facebook phishing demo. Show others how easy it is to replicate Facebook's login to steal credentials. Stay aware, stay safe!\n\n🚫 Educational use only.",
        "link": "https://example.com/phish/facebook"
    },
    "bgmi": {
        "name": "BGMI",
        "emoji": "🎮",
        "caption": "BGMI reward phishing demo to create awareness about common gaming scams. Share with friends for ethical demonstration only.",
        "link": "https://example.com/phish/bgmi"
    },
    "snapchat": {
        "name": "Snapchat",
        "emoji": "👻",
        "caption": "Snapchat login phishing page to show how fake login screens can be made.\n\nAlways double-check URLs before logging in!",
        "link": "https://example.com/phish/snapchat"
    },
    "spotify": {
        "name": "Spotify",
        "emoji": "🎵",
        "caption": "Spotify premium scam awareness demo. Educate users about phishing in streaming platforms.",
        "link": "https://example.com/phish/spotify"
    },
    "gmail": {
        "name": "Gmail",
        "emoji": "📧",
        "caption": "This Gmail phishing demo is to spread awareness of email login scams.\n\nLearn to recognize fake pages before entering sensitive data.",
        "link": "https://example.com/phish/gmail"
    },
}

def setup_phishing_handler(bot: TeleBot):

    @bot.message_handler(func=lambda message: message.text == "🔥 Phishing Pages")
    def phishing_main(message):
        chat_id = message.chat.id
        markup = InlineKeyboardMarkup(row_width=3)

        buttons = [
            InlineKeyboardButton(f"{data['emoji']} {data['name']}", callback_data=f"phish_{key}")
            for key, data in PHISHING_DATA.items()
        ]

        for i in range(0, len(buttons), 3):
            markup.row(*buttons[i:i+3])

        bot.send_photo(
            chat_id,
            photo=PHISHING_IMAGE_URL,
            caption=(
                "🎣 *Phishing Pages Demo Zone*\n\n"
                "Explore realistic phishing clones made for cybersecurity awareness.\n"
                "Click any platform below to view how fake login pages look.\n\n"
                "⚠️ _For ethical hacking learning only. Don't misuse._"
            ),
            parse_mode="Markdown",
            reply_markup=markup
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("phish_"))
    def phishing_page(call):
        chat_id = call.message.chat.id
        key = call.data.split("_")[1]

        if key in PHISHING_DATA:
            data = PHISHING_DATA[key]
            text = (
                f"{data['emoji']} *{data['name']} Phishing Demo*\n\n"
                f"{data['caption']}\n\n"
                f"🔗 *Phishing Page:* `{data['link']}`\n\n"
                f"📬 _You’ll receive the captured details on @H4CKUCATORDATABOT. Please /start it first._"
            )

            link_buttons = InlineKeyboardMarkup()
            link_buttons.add(
                InlineKeyboardButton("🔗 Open Link", url=data['link'])
            )
            link_buttons.add(
                InlineKeyboardButton("🔙 Back to Menu", callback_data="go_back_main")
            )

            # Delete old panel and send new message
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except:
                pass

            bot.send_message(
                chat_id,
                text,
                parse_mode="Markdown",
                disable_web_page_preview=True,
                reply_markup=link_buttons
            )

    @bot.callback_query_handler(func=lambda call: call.data == "go_back_main")
    def go_back_menu(call):
        chat_id = call.message.chat.id

        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

        # Re-show phishing buttons
        markup = InlineKeyboardMarkup(row_width=3)
        buttons = [
            InlineKeyboardButton(f"{data['emoji']} {data['name']}", callback_data=f"phish_{key}")
            for key, data in PHISHING_DATA.items()
        ]
        for i in range(0, len(buttons), 3):
            markup.row(*buttons[i:i+3])

        bot.send_photo(
            chat_id,
            photo=PHISHING_IMAGE_URL,
            caption=(
                "🎣 *Phishing Pages Demo Zone*\n\n"
                "Explore realistic phishing clones made for cybersecurity awareness.\n"
                "Click any platform below to view how fake login pages look.\n\n"
                "⚠️ _For ethical hacking learning only. Don't misuse._"
            ),
            parse_mode="Markdown",
            reply_markup=markup
        )


