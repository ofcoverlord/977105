import requests
from telebot import types
from utils import can_use_osint, add_osint_usage, get_remaining_uses, get_referral_link

def setup_osint_handler(bot, user_modes):
    @bot.message_handler(commands=['osint'])
    def osint_entry(msg):
        user_id = msg.from_user.id

        if not can_use_osint(user_id):
            referral = get_referral_link(user_id)
            bot.send_message(msg.chat.id, f"🚫 You've reached your OSINT limit. Invite 3 friends to get more scans!\n\n🔗 Your referral link:\n{referral}")
            return

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('🔍 Lookup Username', '📞 Phone Number Info')
        markup.row('📧 Email Breach Check', '🏠 Main Menu')
        bot.send_message(msg.chat.id, "🧠 *Welcome to OSINT Auto Suite!*\nChoose an action:", parse_mode='Markdown', reply_markup=markup)
        user_modes[msg.chat.id] = 'menu_osint'

    @bot.message_handler(func=lambda msg: user_modes.get(msg.chat.id) == 'menu_osint')
    def osint_mode_selector(msg):
        text = msg.text.lower()
        if 'username' in text:
            bot.send_message(msg.chat.id, "📝 Send the *username* you want to investigate:", parse_mode='Markdown')
            user_modes[msg.chat.id] = 'osint_username'
        elif 'phone' in text:
            bot.send_message(msg.chat.id, "📲 Send the *phone number* (with country code) to trace:", parse_mode='Markdown')
            user_modes[msg.chat.id] = 'osint_phone'
        elif 'email' in text:
            bot.send_message(msg.chat.id, "📧 Send the *email address* to check for leaks:", parse_mode='Markdown')
            user_modes[msg.chat.id] = 'osint_email'
        elif 'menu' in text:
            from menu import show_main_menu
            show_main_menu(bot, msg)
        else:
            bot.send_message(msg.chat.id, "❓ Invalid option. Please use the keyboard.")

    @bot.message_handler(func=lambda msg: user_modes.get(msg.chat.id) in ['osint_username', 'osint_phone', 'osint_email'])
    def handle_osint_input(msg):
        mode = user_modes.get(msg.chat.id)
        query = msg.text.strip()
        user_id = msg.from_user.id

        bot.send_chat_action(msg.chat.id, 'typing')

        if mode == 'osint_username':
            handle_username_lookup(bot, msg, query)
        elif mode == 'osint_phone':
            handle_phone_lookup(bot, msg, query)
        elif mode == 'osint_email':
            handle_email_lookup(bot, msg, query)

        add_osint_usage(user_id)
        left = get_remaining_uses(user_id)
        bot.send_message(msg.chat.id, f"✨ Remaining OSINT scans: {left}")
        user_modes[msg.chat.id] = 'menu_osint'

def handle_username_lookup(bot, msg, username):
    if username.startswith('@'):
        username = username[1:]

    # Instagram Info
    insta_url = f"https://instainfo.rishuapi.workers.dev/info?username={username}"
    r = requests.get(insta_url)
    if r.status_code != 200 or 'username' not in r.text:
        bot.send_message(msg.chat.id, "⚠️ Instagram lookup failed. Try again later.")
        return

    data = r.json()
    result = f"👤 *Instagram Info*\n"
    result += f"▫️ Name: {data.get('full_name', 'N/A')}\n"
    result += f"▫️ Username: @{data.get('username')}\n"
    result += f"▫️ Bio: {data.get('biography', 'N/A')}\n"
    result += f"▫️ Followers: {data.get('followers')} | Following: {data.get('following')}\n"
    result += f"📸 Posts: {data.get('posts')}\n"
    result += f"🔗 Profile: https://instagram.com/{username}"
    bot.send_message(msg.chat.id, result, parse_mode="Markdown")

def handle_phone_lookup(bot, msg, phone):
    api_url = f"https://truecaller.privates-bots.workers.dev/?q={phone}"
    try:
        res = requests.get(api_url)
        data = res.json()

        if not data or 'name' not in data:
            bot.send_message(msg.chat.id, "❌ No data found for this number.")
            return

        result = f"📞 *Phone Number Details*\n"
        result += f"👤 Name: {data.get('name', 'N/A')}\n"
        result += f"🌐 Country: {data.get('country', 'N/A')}\n"
        result += f"🏷️ Carrier: {data.get('carrier', 'N/A')}\n"

        # Remove developer info if any
        links = []
        if data.get("telegram"):
            links.append(f"✈️ Telegram: {data['telegram']}")
        if data.get("whatsapp"):
            links.append(f"💬 WhatsApp: {data['whatsapp']}")
        if data.get("twitter"):
            links.append(f"🐦 Twitter: {data['twitter']}")

        if links:
            result += "\n" + "\n".join(links)

        bot.send_message(msg.chat.id, result, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Error fetching number details.")


def handle_email_lookup(bot, msg, email):
    url = f"https://soxoj-api.vercel.app/api/email/{email}"
    try:
        r = requests.get(url)
        data = r.json()

        if not data.get('data'):
            bot.send_message(msg.chat.id, "❌ No leaks found or email is invalid.")
            return

        result = f"📧 *Email Breach Report*\n\n"
        for site in data['data']:
            result += f"🛑 {site}\n"

        bot.send_message(msg.chat.id, result, parse_mode="Markdown")
    except:
        bot.send_message(msg.chat.id, "⚠️ Could not check email breaches at the moment.")

