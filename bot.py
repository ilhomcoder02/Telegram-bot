from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

ADMIN_ID = 7199653464  # Sizning Telegram ID'ingiz

# Foydalanuvchi yuborganini admin (siz)ga yuborish
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    msg = update.message

    if user.id == ADMIN_ID:
        return  # Admin yozsa o‘ziga yubormaydi

    header = f"[#{user.id}] {user.first_name} (@{user.username if user.username else 'username yo‘q'})"

    if msg.text:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"{header}:
{msg.text}")
    elif msg.photo:
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=msg.photo[-1].file_id, caption=header + " (rasm)")
    elif msg.video:
        await context.bot.send_video(chat_id=ADMIN_ID, video=msg.video.file_id, caption=header + " (video)")
    elif msg.document:
        await context.bot.send_document(chat_id=ADMIN_ID, document=msg.document.file_id, caption=header + " (fayl)")
    elif msg.sticker:
        await context.bot.send_sticker(chat_id=ADMIN_ID, sticker=msg.sticker.file_id)
    elif msg.animation:
        await context.bot.send_animation(chat_id=ADMIN_ID, animation=msg.animation.file_id, caption=header + " (GIF)")

# Admin reply qilganda foydalanuvchiga javob berish
async def handle_admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if update.effective_chat.id != ADMIN_ID or not msg.reply_to_message:
        return

    original_text = msg.reply_to_message.text or msg.reply_to_message.caption
    if "[#" not in original_text or "]" not in original_text:
        return

    try:
        user_id_str = original_text.split("[#")[1].split("]")[0]
        user_id = int(user_id_str)

        if msg.text:
            await context.bot.send_message(chat_id=user_id, text=msg.text)
        elif msg.photo:
            await context.bot.send_photo(chat_id=user_id, photo=msg.photo[-1].file_id, caption=msg.caption)
        elif msg.video:
            await context.bot.send_video(chat_id=user_id, video=msg.video.file_id, caption=msg.caption)
        elif msg.document:
            await context.bot.send_document(chat_id=user_id, document=msg.document.file_id, caption=msg.caption)
        elif msg.sticker:
            await context.bot.send_sticker(chat_id=user_id, sticker=msg.sticker.file_id)
        elif msg.animation:
            await context.bot.send_animation(chat_id=user_id, animation=msg.animation.file_id, caption=msg.caption)
    except Exception as e:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Xatolik: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Xabar yuboring.")

if __name__ == '__main__':
    TOKEN = "8012729420:AAGGjkPZ5Ok_I456UdXoY2BsYJUFMS0eBq4"
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE, forward_to_admin))
    app.add_handler(MessageHandler(filters.ALL, handle_admin_reply))

    print("Bot ishga tushdi...")
    app.run_polling()