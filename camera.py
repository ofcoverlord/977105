from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot
from start import show_main_menu

def setup_camera_handler(bot: TeleBot):

    @bot.message_handler(func=lambda message: message.text == "📸 Camera Demo")
    def camera_demo(msg):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📸 Try Camera Access Demo", url="https://www.onlinemictest.com/webcam-test/"))
        markup.add(InlineKeyboardButton("🔙 Back to Menu", callback_data="go_back_main"))

        bot.send_message(
            msg.chat.id,
            "📷 *Test Camera Access* (Educational Only)\n\n"
            "Use this tool to understand how websites may try to access your camera via browser permissions.\n"
            "Try the demo and observe how permission prompts work.\n\n"
            "⚠️ *Never allow access on untrusted websites!*\n"
            "Use this for learning purpose only. Stay secure! 🔐",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data == "go_back_main")
    def go_back_to_menu(call):
        show_main_menu(call.message.chat.id)
