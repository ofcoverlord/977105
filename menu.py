from telebot.types import ReplyKeyboardMarkup, KeyboardButton

ADMIN_ID = 7407431042  # ✅ Replace with your Telegram user ID

def show_main_menu(bot, chat_id):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # ✅ Only add buttons for all users
    keyboard.add(
        KeyboardButton("🔥 Phishing Pages"),
        KeyboardButton("🕵️ OSINT Tools")
    )
    keyboard.add(
        KeyboardButton("📷 Camera Demo"),
        KeyboardButton("📍 Location Demo")
    )

    # ✅ Add "Broadcast" button only for admin
    if chat_id == ADMIN_ID:
        keyboard.add(KeyboardButton("📢 Broadcast"))

    bot.send_message(chat_id, "Choose an option:", reply_markup=keyboard)

