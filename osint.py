import requests
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("osint") & filters.private)
async def osint_info(client, message: Message):
    await message.reply_text(
        "📞 *Phone Number Lookup (Truecaller OSINT)*\n\n"
        "Send me any mobile number with country code like this:\n"
        "`+919876543210`\n\n"
        "I’ll instantly find:\n"
        "🔹 SIM Owner Name\n"
        "🔹 Location & Carrier Info\n"
        "🔹 Timezone and More\n\n"
        "_Powered by @BotNations 🔥_"
    )


@Client.on_message(filters.text & filters.private)
async def lookup_number(client, message: Message):
    number = message.text.strip()

    if not number.startswith("+") or not number[1:].isdigit():
        return await message.reply_text("❌ Please send a valid phone number with country code (e.g. `+918888888888`)")

    try:
        api_url = f"https://truecaller.privates-bots.workers.dev/?q={number}"
        response = requests.get(api_url, timeout=10)
        data = response.json()

        # If basic validation fails
        if not data or "carrier" not in data:
            return await message.reply_text("❌ No details found for this number.")

        reply = f"🔍 *Truecaller Lookup Result*\n\n"
        reply += f"📱 *Number:* `{data.get('international_format', number)}`\n"
        reply += f"👤 *Name:* `{data.get('Truecaller') or data.get('Unknown', 'N/A')}`\n"
        reply += f"🌐 *Location:* `{data.get('location', 'N/A')}`\n"
        reply += f"📶 *Carrier:* `{data.get('carrier', 'N/A')}`\n"
        reply += f"🕓 *Timezone:* `{', '.join(data.get('timezones', ['N/A']))}`\n"
        reply += f"🏳️ *Country:* `{data.get('country', 'N/A')}`\n\n"
        reply += "_OSINT powered by @H4CKUCATOR 💀_"

        await message.reply_text(reply)

    except Exception as e:
        await message.reply_text(f"⚠️ API Error: `{str(e)}`\nPlease try again later.")
