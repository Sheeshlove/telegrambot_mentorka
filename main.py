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

# English: States for conversation
# Russian: Состояния для разговора
class States:
    MAIN_MENU = 0
    SNILS = 1
    FIO = 2
    DOB = 3

# English: User states storage
# Russian: Хранилище состояний пользователей
user_states = {}

# English: Get main menu keyboard
# Russian: Получение клавиатуры главного меню
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton("Чат первокурсников"),
        types.KeyboardButton("Помощь ментора")
    )
    keyboard.row(types.KeyboardButton("/start"))
    return keyboard

# English: Start command handler
# Russian: Обработчик команды старт
@bot.message_handler(commands=['start'])
def start(message):
    # English: Clear user state and data
    # Russian: Очистка состояния и данных пользователя
    user_id = message.from_user.id
    user_states[user_id] = States.MAIN_MENU
    
    # English: Get user's first name for personal greeting
    # Russian: Получение имени пользователя для персонального приветствия
    user_name = message.from_user.first_name
    
    # English: Send welcome message
    # Russian: Отправка приветственного сообщения
    bot.send_message(
        message.chat.id,
        f"👋 Привет, {user_name}!\n\n"
        "Я бот-помощник. Чем могу помочь?\n\n"
        "• Нажмите 'Чат первокурсников' для доступа к чату\n"
        "• Нажмите 'Помощь ментора' для связи с ментором\n"
        "• В любой момент можете нажать /start для возврата в главное меню",
        reply_markup=get_main_keyboard()
    )

# English: Main menu handler
# Russian: Обработчик главного меню
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == States.MAIN_MENU)
def main_menu(message):
    if message.text == "Чат первокурсников":
        user_states[message.from_user.id] = States.SNILS
        bot.send_message(
            message.chat.id,
            "Для доступа к чату первокурсников, пожалуйста, введите ваш СНИЛС\n"
            "Формат: XXX-XXX-XXX XX\n"
            "Например: 123-456-789 00"
        )
    elif message.text == "Помощь ментора":
        bot.send_message(
            message.chat.id,
            "👨‍🏫 Для получения помощи от ментора, пожалуйста, напишите:\n"
            "@sheeshlove\n\n"
            "Для возврата в главное меню нажмите /start",
            reply_markup=get_main_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, используйте кнопки меню для навигации.",
            reply_markup=get_main_keyboard()
        )

# English: SNILS input handler
# Russian: Обработчик ввода СНИЛС
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == States.SNILS)
def get_snils(message):
    from utils.validators import validate_snils
    
    if not validate_snils(message.text):
        bot.send_message(
            message.chat.id,
            "❌ Неверный формат СНИЛС!\n"
            "Пожалуйста, введите СНИЛС в формате: XXX-XXX-XXX XX\n"
            "Например: 123-456-789 00"
        )
        return
    
    # English: Store SNILS and move to FIO state
    # Russian: Сохранение СНИЛС и переход к состоянию ФИО
    user_states[message.from_user.id] = States.FIO
    bot.send_message(message.chat.id, "Теперь введите ваше ФИО (как в паспорте):")

# English: FIO input handler
# Russian: Обработчик ввода ФИО
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == States.FIO)
def get_fio(message):
    from utils.validators import validate_fio
    
    if not validate_fio(message.text):
        bot.send_message(
            message.chat.id,
            "❌ Пожалуйста, введите полное ФИО (Фамилия Имя Отчество)"
        )
        return
    
    # English: Store FIO and move to DOB state
    # Russian: Сохранение ФИО и переход к состоянию даты рождения
    user_states[message.from_user.id] = States.DOB
    bot.send_message(
        message.chat.id,
        "Введите вашу дату рождения в формате YYYY-MM-DD\n"
        "Например: 2000-01-01"
    )

# English: Date of birth input handler
# Russian: Обработчик ввода даты рождения
@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == States.DOB)
def get_dob(message):
    from utils.validators import validate_date
    from database.mock_data import DATABASE
    
    if not validate_date(message.text):
        bot.send_message(
            message.chat.id,
            "❌ Неверный формат даты!\n"
            "Пожалуйста, используйте формат: YYYY-MM-DD\n"
            "Например: 2000-01-01"
        )
        return
    
    # English: Check user data in database
    # Russian: Проверка данных пользователя в базе
    user_found = None
    for entry in DATABASE:
        if (entry["snils"] == message.text and
            entry["fio"] == message.text and
            entry["dob"] == message.text):
            user_found = entry
            break

    if user_found:
        bot.send_message(
            message.chat.id,
            "✅ Данные подтверждены!\n\n"
            "Ссылка на чат первокурсников: [будет добавлена позже]\n\n"
            "Для возврата в главное меню нажмите /start",
            reply_markup=get_main_keyboard()
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ К сожалению, ваши данные не найдены в базе.\n"
            "Пожалуйста, проверьте введенные данные и попробуйте снова.\n\n"
            "Для возврата в главное меню нажмите /start",
            reply_markup=get_main_keyboard()
        )
    
    # English: Reset user state
    # Russian: Сброс состояния пользователя
    user_states[message.from_user.id] = States.MAIN_MENU

# English: Run the bot
# Russian: Запуск бота
if __name__ == '__main__':
    print("Bot started...")
    bot.infinity_polling() 