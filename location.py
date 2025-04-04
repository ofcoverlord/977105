from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot
from start import show_main_menu

def setup_location_handler(bot: TeleBot):

    @bot.message_handler(func=lambda message: message.text == "📍 Location Demo")
    def location_demo(msg):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📍 Try Location Access Demo", url="https://mylocation.org/"))
        markup.add(InlineKeyboardButton("🔙 Back to Menu", callback_data="go_back_main"))

        bot.send_message(
            msg.chat.id,
            "📍 *Location Tracker Awareness* (For Education Only)\n\n"
            "This demo shows how websites can ask for your device's location.\n"
            "Tap the button below to test in your browser and understand how geolocation works.\n\n"
            "⚠️ *Avoid allowing unknown websites to access your location!*\n"
            "Always review permissions before granting access. 🛡️",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data == "go_back_main")
    def go_back_to_menu(call):
        show_main_menu(call.message.chat.id)
