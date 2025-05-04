import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# .env o'zgaruvchilar
TOKEN = os.getenv("8012729420:AAGNWaNGikQ_bSLym8MOEeLk-2gGnLLFFUY")
ADMIN_ID = int(os.getenv("7199653464"))

# /start komandasi
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Assalamu alayk, {user.first_name}!\n"
        "Men sizning habaringizni Zubayrga yetkazishga yordam beraman."
    )

# Foydalanuvchi yuborgan xabarni administratorga yuborish
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.effective_message

    header = f"[{user.id}] {user.full_name}"
    if user.username:
        header += f" (@{user.username})"

    await context.bot.send_message(chat_id=ADMIN_ID, text=header)
    await message.copy(chat_id=ADMIN_ID)

# Admin reply orqali foydalanuvchiga javob berishi
async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        original_text = update.message.reply_to_message.text
        user_id = None
        if original_text and original_text.startswith('['):
            try:
                user_id = int(original_text.split(']')[0][1:])
            except:
                pass
        if user_id:
            await context.bot.send_message(chat_id=user_id, text=update.message.text)

# Botni ishga tushirish
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), forward_to_admin))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, reply_to_user))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
