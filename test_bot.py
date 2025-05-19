import telebot
from telebot import types
import os
from dotenv import load_dotenv

# English: Load environment variables
# Russian: Загрузка переменных окружения
load_dotenv()

# English: Initialize bot with token
# Russian: Инициализация бота с токеном
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7223734470:AAGoQflInEfUz5APYflFb1BciDwyTqNK-II')
bot = telebot.TeleBot(TOKEN)

# English: Simple keyboard
# Russian: Простая клавиатура
def get_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("Привет"), types.KeyboardButton("Помощь"))
    return keyboard

# English: Start command handler
# Russian: Обработчик команды старт
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        f"👋 Привет, {user_name}!\n\n"
        "Я тестовый бот. Нажмите кнопку 'Привет' или 'Помощь'",
        reply_markup=get_keyboard()
    )

# English: Text message handler
# Russian: Обработчик текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Привет":
        bot.send_message(
            message.chat.id,
            "Привет! Как я могу помочь?",
            reply_markup=get_keyboard()
        )
    elif message.text == "Помощь":
        bot.send_message(
            message.chat.id,
            "Это тестовый бот. Используйте команду /start для начала работы.",
            reply_markup=get_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, используйте кнопки или команду /start",
            reply_markup=get_keyboard()
        )

# English: Run the bot
# Russian: Запуск бота
if __name__ == '__main__':
    print("Test bot started...")
    bot.infinity_polling() 