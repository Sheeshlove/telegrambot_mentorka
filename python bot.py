import random
import os
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Load token from environment variable for security
# English: Loading bot token from environment variable for better security
# Russian: Загрузка токена бота из переменной окружения для лучшей безопасности
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7223734470:AAGoQflInEfUz5APYflFb1BciDwyTqNK-II')

# English: Database with random data for testing
# Russian: База данных с тестовыми данными
DATABASE = [
    {"snils": "123-45-6789", "fio": "Иванов Иван Иванович", "dob": "2000-01-01"},
    {"snils": "987-65-4321", "fio": "Петров Петр Петрович", "dob": "1999-02-15"},
    {"snils": "555-44-3333", "fio": "Сидоров Сидор Сидорович", "dob": "1998-03-25"},
    {"snils": "444-33-2222", "fio": "Козлов Алексей Александрович", "dob": "2001-04-30"},
    {"snils": "111-22-3333", "fio": "Алексеева Мария Николаевна", "dob": "1997-05-10"},
    {"snils": "333-22-4444", "fio": "Смирнова Ольга Викторовна", "dob": "1996-06-20"},
    {"snils": "666-77-8888", "fio": "Тимофеев Артем Сергеевич", "dob": "1995-07-05"},
    {"snils": "999-88-7777", "fio": "Гордеев Павел Васильевич", "dob": "2002-08-15"},
    {"snils": "222-33-4444", "fio": "Романов Сергей Павлович", "dob": "1998-09-25"},
    {"snils": "777-66-5555", "fio": "Барсова Анна Викторовна", "dob": "1999-10-05"}
]

# English: Conversation states
# Russian: Состояния разговора
MAIN_MENU, SNILS, FIO, DOB = range(4)

# English: Validation functions
# Russian: Функции валидации
def validate_snils(snils: str) -> bool:
    # English: Validate SNILS format (XXX-XXX-XXX XX)
    # Russian: Проверка формата СНИЛС (XXX-XXX-XXX XX)
    import re
    pattern = r'^\d{3}-\d{3}-\d{3} \d{2}$'
    return bool(re.match(pattern, snils))

def validate_date(date_str: str) -> bool:
    # English: Validate date format (YYYY-MM-DD)
    # Russian: Проверка формата даты (YYYY-MM-DD)
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# English: Main menu keyboard
# Russian: Клавиатура главного меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("Чат первокурсников"), KeyboardButton("Помощь ментора")],
        [KeyboardButton("/start")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# English: Start command handler
# Russian: Обработчик команды старт
def start(update: Update, context: CallbackContext) -> int:
    # English: Clear any existing user data
    # Russian: Очистка существующих данных пользователя
    context.user_data.clear()
    
    update.message.reply_text(
        "👋 Привет! Я бот-помощник для первокурсников.\n\n"
        "Выберите нужный раздел:",
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.HTML
    )
    return MAIN_MENU

# English: Main menu handler
# Russian: Обработчик главного меню
def main_menu(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    
    if text == "Чат первокурсников":
        update.message.reply_text(
            "Для доступа к чату первокурсников, пожалуйста, введите ваш СНИЛС\n"
            "Формат: XXX-XXX-XXX XX\n"
            "Например: 123-456-789 00"
        )
        return SNILS
    elif text == "Помощь ментора":
        return mentor_help(update, context)
    else:
        update.message.reply_text(
            "Пожалуйста, используйте кнопки меню для навигации.",
            reply_markup=get_main_keyboard()
        )
        return MAIN_MENU

# English: SNILS input handler
# Russian: Обработчик ввода СНИЛС
def get_snils(update: Update, context: CallbackContext) -> int:
    user_snils = update.message.text
    
    if not validate_snils(user_snils):
        update.message.reply_text(
            "❌ Неверный формат СНИЛС!\n"
            "Пожалуйста, введите СНИЛС в формате: XXX-XXX-XXX XX\n"
            "Например: 123-456-789 00"
        )
        return SNILS
    
    context.user_data["snils"] = user_snils
    update.message.reply_text("Теперь введите ваше ФИО (как в паспорте):")
    return FIO

# English: FIO input handler
# Russian: Обработчик ввода ФИО
def get_fio(update: Update, context: CallbackContext) -> int:
    user_fio = update.message.text.strip()
    
    if len(user_fio.split()) < 2:
        update.message.reply_text(
            "❌ Пожалуйста, введите полное ФИО (Фамилия Имя Отчество)"
        )
        return FIO
    
    context.user_data["fio"] = user_fio
    update.message.reply_text(
        "Введите вашу дату рождения в формате YYYY-MM-DD\n"
        "Например: 2000-01-01"
    )
    return DOB

# English: Date of birth input handler
# Russian: Обработчик ввода даты рождения
def get_dob(update: Update, context: CallbackContext) -> int:
    user_dob = update.message.text
    
    if not validate_date(user_dob):
        update.message.reply_text(
            "❌ Неверный формат даты!\n"
            "Пожалуйста, используйте формат: YYYY-MM-DD\n"
            "Например: 2000-01-01"
        )
        return DOB
    
    context.user_data["dob"] = user_dob
    return check_user_data(update, context)

# English: User data verification
# Russian: Проверка данных пользователя
def check_user_data(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_found = None
    
    for entry in DATABASE:
        if (entry["snils"] == user_data.get("snils") and
            entry["fio"] == user_data.get("fio") and
            entry["dob"] == user_data.get("dob")):
            user_found = entry
            break

    if user_found:
        update.message.reply_text(
            "✅ Данные подтверждены!\n\n"
            "Ссылка на чат первокурсников: [будет добавлена позже]\n\n"
            "Для возврата в главное меню нажмите /start",
            reply_markup=get_main_keyboard()
        )
    else:
        update.message.reply_text(
            "❌ К сожалению, ваши данные не найдены в базе.\n"
            "Пожалуйста, проверьте введенные данные и попробуйте снова.\n\n"
            "Для возврата в главное меню нажмите /start",
            reply_markup=get_main_keyboard()
        )
    
    context.user_data.clear()
    return MAIN_MENU

# English: Mentor help handler
# Russian: Обработчик помощи ментора
def mentor_help(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "👨‍🏫 Для получения помощи от ментора, пожалуйста, напишите:\n"
        "@sheeshlove\n\n"
        "Для возврата в главное меню нажмите /start",
        reply_markup=get_main_keyboard()
    )
    return MAIN_MENU

# English: Cancel command handler
# Russian: Обработчик команды отмены
def cancel(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    update.message.reply_text(
        "До свидания! Для начала работы нажмите /start",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

# English: Main function to run the bot
# Russian: Главная функция для запуска бота
def main():
    # English: Initialize bot and dispatcher
    # Russian: Инициализация бота и диспетчера
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # English: Add conversation handler
    # Russian: Добавление обработчика разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [
                MessageHandler(Filters.text & ~Filters.command, main_menu)
            ],
            SNILS: [
                MessageHandler(Filters.text & ~Filters.command, get_snils)
            ],
            FIO: [
                MessageHandler(Filters.text & ~Filters.command, get_fio)
            ],
            DOB: [
                MessageHandler(Filters.text & ~Filters.command, get_dob)
            ]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    
    # English: Start the bot
    # Russian: Запуск бота
    print("Bot started...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
