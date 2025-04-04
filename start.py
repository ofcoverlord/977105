from verify import send_verification_instructions
from menu import show_main_menu
from user_db import add_referral
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

HACKING_IMAGE_URL = "https://t.me/PHOTOUPLOAD22/2"

def setup_start_handler(bot, users, user_modes):  # ✅ FIXED: now accepts 3 args
    @bot.message_handler(commands=['start'])
    def start(message):
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)

        user_modes.pop(chat_id, None)  # ✅ Optional: reset mode on /start

        # ✅ Referral logic
        if " " in message.text:
            ref_id = message.text.split()[1]
            if ref_id != user_id:
                add_referral(ref_id, user_id)

        # ✅ Initialize user
        if chat_id not in users:
            users[chat_id] = {
                "uses_left": 1,
                "referrals": [],
                "joined": False
            }

        if not users[chat_id]["joined"]:
            bot.send_photo(chat_id, HACKING_IMAGE_URL,
                caption="👾 *Welcome to H4ckers Adda Bot* 👾\n\n🔐 Educational Purpose Only!\n🔗 Please join our channel and verify.",
                parse_mode="Markdown")
            send_verification_instructions(bot, chat_id)
        else:
            show_main_menu(bot, chat_id)
