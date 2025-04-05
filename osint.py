from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import requests

# Session flag to activate OSINT only when button is clicked
user_osint_mode = {}

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    user_id = message.from_user.id
    user_osint_mode[user_id] = False  # Reset mode on /start

    await message.reply_photo(
        photo="https://te.legra.ph/file/99db62ad5f6c9d67695b8.jpg",  # Optional image
        caption="👾 *Welcome to H4ckers Adda Bot*\n\n"
                "🔐 Educational Purpose Only!\n\n"
                "Click below to begin exploring tools like OSINT!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🕵️ OSINT Tools", callback_data="osint_menu")]
        ])
    )


@Client.on_callback_query(filters.regex("osint_menu"))
async def osint_menu_handler(client, callback_query):
    user_id = callback_query.from_user.id
    user_osint_mode[user_id] = True  # Enable OSINT mode

    await callback_query.message.edit_text(
        "🕵️‍♂️ *OSINT Tools Enabled!*\n\n"
        "Now send any of the following:\n"
        "`+91xxxxxxxxxx` (Phone)\n"
        "`someone@email.com` (Email)\n"
        "`username123` (Username)\n\n"
        "_I’ll fetch public data from various sources!_"
    )


@Client.on_message(filters.text & filters.private)
async def osint_processor(client, message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    # ✅ 1. Only proceed if OSINT mode is active
    if not user_osint_mode.get(user_id, False):
        return await message.reply("❌ Invalid format. Please send a valid phone, email, or username.\n(Click *OSINT Tools* to activate this feature)")

    # ✅ 2. Phone number processing
    if text.isdigit() or text.startswith("+91"):
        number = text
        if not number.startswith("+"):
            number = f"+91{number}"

        try:
            url = f"https://truecaller.privates-bots.workers.dev/?q={number}"
            res = requests.get(url)
            data = res.json()

            if not data or "carrier" not in data:
                return await message.reply("❌ No data found for this number.")

            reply = f"📞 *Truecaller Lookup*\n\n"
            reply += f"👤 *Name:* `{data.get('Truecaller', 'N/A')}`\n"
            reply += f"📍 *Location:* `{data.get('location', 'N/A')}`\n"
            reply += f"📶 *Carrier:* `{data.get('carrier', 'N/A')}`\n"
            reply += f"🌐 *Timezone:* `{', '.join(data.get('timezones', ['N/A']))}`\n"
            reply += f"🏳️ *Country:* `{data.get('country', 'N/A')}`\n"

            return await message.reply_text(reply)

        except Exception as e:
            return await message.reply(f"⚠️ API Error: `{str(e)}`")

    else:
        return await message.reply("❌ Invalid phone number. Please enter a valid number (e.g. `+919999999999`).")

