from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database import save_user  # Make sure this saves the full users dict

def setup_verification_handler(bot, users):
    @bot.message_handler(func=lambda msg: msg.text == "I've Joined")
    def verify(msg):
        chat_id = str(msg.chat.id)
        print(f"🛂 Received 'I've Joined' from {chat_id}")
        
        if chat_id in users:
            users[chat_id]["joined"] = True
            try:
                save_user(users)
                print(f"✅ User {chat_id} marked as joined.")
            except Exception as e:
                print(f"❌ Error saving user {chat_id}: {e}")
            
            bot.send_message(chat_id, "✅ Verified! Now type /start to begin.")
        else:
            print(f"⚠️ User {chat_id} tried verifying without using /start")
            bot.send_message(chat_id, "❌ Please use /start first to register.")

def send_verification_instructions(bot, chat_id):
    print(f"📩 Sending verification instructions to {chat_id}")
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("I've Joined"))
    bot.send_message(
        chat_id,
        "📢 Please join our Telegram channel first, then click the button below.",
        reply_markup=markup
    )

