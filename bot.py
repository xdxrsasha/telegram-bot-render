 import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Токен и ID из environment variables
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен! Пиши, что хочешь, я передам админу.")

# Обработчик текстовых сообщений
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username if user.username else "Без username"
    message_text = update.message.text

    # Отправка сообщения админу
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Сообщение от @{username}:\n{message_text}"
    )

# Обработчик стикеров
async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    username = user.username if user.username else "Без username"
    sticker = update.message.sticker
    sticker_id = sticker.file_id if sticker else "Неизвестный стикер"

    # Отправка информации о стикере админу
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Стикер от @{username}:\n[Стикер] (ID: {sticker_id})"
    )

def main():
    # Создаем приложение
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.Sticker, handle_sticker))

    # Запускаем бота
    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
