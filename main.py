from flask import Flask
from threading import Thread
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import os

app = Flask('')

TOKEN = os.environ.get('8025520566:AAGx3shIkdZ9EoLj8uUmA7Iu6uojr07_7NY')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data='stats')],
        [InlineKeyboardButton("📋 Создать опрос", callback_data='poll')],
        [InlineKeyboardButton("🎁 Конкурс", callback_data='contest')],
        [InlineKeyboardButton("⏰ Автопостинг", callback_data='schedule')],
        [InlineKeyboardButton("⚙️ Настройки", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('🤖 Привет! Выбери функцию:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == 'stats':
        query.message.reply_text('📊 Отправь @username канала')
    elif query.data == 'poll':
        query.message.reply_text('📋 Отправь: Вопрос | Вариант1 | Вариант2')
    elif query.data == 'contest':
        query.message.reply_text('🎁 Отправь: количество | ссылка на пост')
    elif query.data == 'schedule':
        query.message.reply_text('⏰ В разработке')
    elif query.data == 'settings':
        query.message.reply_text('⚙️ Добавь меня админом в канал')

def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    
    if text.startswith('@'):
        channel = text.replace('@', '')
        update.message.reply_text(
            f"📊 Канал @{channel}\n"
            f"Ссылка: https://t.me/{channel}\n"
            f"Статистика: https://telemetr.me/{channel}"
        )
    elif '|' in text:
        parts = [p.strip() for p in text.split('|')]
        if len(parts) >= 3:
            question = parts[0]
            options = parts[1:]
            update.message.reply_poll(question=question, options=options)
        else:
            update.message.reply_text("❌ Минимум 2 варианта через |")
    else:
        update.message.reply_text("Выбери команду в меню 👇")

def main():
    keep_alive()
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
      
