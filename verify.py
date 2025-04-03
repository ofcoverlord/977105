from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from utils.database import save_user  # ✅ Correct import

def setup_verification_handler(bot, users):
    @bot.message_handler(func=lambda msg: msg.text == "I've Joined")
    def verify(msg):
        chat_id = str(msg.chat.id)
        if chat_id in users:
            users[chat_id]["joined"] = True
            save_user(users)  # ✅ Updated function call
            bot.send_message(chat_id, "✅ Verified! Use /start to continue.")
        else:
            bot.send_message(chat_id, "❌ Please use /start first to register.")

def send_verification_instructions(bot, chat_id):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("I've Joined"))
    bot.send_message(chat_id, "👉 Join our channel then click 'I've Joined'", reply_markup=markup)
