def setup_broadcast_handler(bot, users, admin_id):
    @bot.message_handler(func=lambda m: m.text == "📢 Broadcast" and m.from_user.id == admin_id)
    def ask_broadcast(msg):
        bot.send_message(msg.chat.id, "📣 Send the message/photo/video to broadcast.")

        @bot.message_handler(content_types=['text', 'photo', 'video'])
        def do_broadcast(m):
            for uid in list(users):
                try:
                    if m.content_type == "text":
                        bot.send_message(uid, m.text)
                    elif m.content_type == "photo":
                        bot.send_photo(uid, m.photo[-1].file_id, caption=m.caption)
                    elif m.content_type == "video":
                        bot.send_video(uid, m.video.file_id, caption=m.caption)
                except:
                    users.pop(uid)
            from utils.database import save_user
            save_user(users)
            bot.send_message(m.chat.id, "✅ Broadcast Done.")