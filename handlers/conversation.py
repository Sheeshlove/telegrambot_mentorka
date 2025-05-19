from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ParseMode
from telegram.ext import CallbackContext, ConversationHandler

from config.config import Config
from database.mock_data import DATABASE
from utils.validators import validate_snils, validate_fio, validate_date

# English: Get main menu keyboard
# Russian: Получение клавиатуры главного меню
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
    
    # English: Get user's first name for personal greeting
    # Russian: Получение имени пользователя для персонального приветствия
    user_name = update.effective_user.first_name
    
    # English: Send welcome message
    # Russian: Отправка приветственного сообщения
    update.message.reply_text(
        f"👋 Привет, {user_name}!\n\n"
        "Я бот-помощник. Чем могу помочь?\n\n"
        "• Нажмите 'Чат первокурсников' для доступа к чату\n"
        "• Нажмите 'Помощь ментора' для связи с ментором\n"
        "• В любой момент можете нажать /start для возврата в главное меню",
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.HTML
    )
    return Config.MAIN_MENU

# English: Main menu handler
# Russian: Обработчик главного меню
def main_menu(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    
    if text == "Чат первокурсников":
        update.message.reply_text(Config.MESSAGES['snils_format'])
        return Config.SNILS
    elif text == "Помощь ментора":
        return mentor_help(update, context)
    else:
        update.message.reply_text(
            "Пожалуйста, используйте кнопки меню для навигации.",
            reply_markup=get_main_keyboard()
        )
        return Config.MAIN_MENU

# English: SNILS input handler
# Russian: Обработчик ввода СНИЛС
def get_snils(update: Update, context: CallbackContext) -> int:
    user_snils = update.message.text
    
    if not validate_snils(user_snils):
        update.message.reply_text(Config.MESSAGES['invalid_snils'])
        return Config.SNILS
    
    context.user_data["snils"] = user_snils
    update.message.reply_text("Теперь введите ваше ФИО (как в паспорте):")
    return Config.FIO

# English: FIO input handler
# Russian: Обработчик ввода ФИО
def get_fio(update: Update, context: CallbackContext) -> int:
    user_fio = update.message.text.strip()
    
    if not validate_fio(user_fio):
        update.message.reply_text(Config.MESSAGES['invalid_fio'])
        return Config.FIO
    
    context.user_data["fio"] = user_fio
    update.message.reply_text(
        "Введите вашу дату рождения в формате YYYY-MM-DD\n"
        "Например: 2000-01-01"
    )
    return Config.DOB

# English: Date of birth input handler
# Russian: Обработчик ввода даты рождения
def get_dob(update: Update, context: CallbackContext) -> int:
    user_dob = update.message.text
    
    if not validate_date(user_dob):
        update.message.reply_text(Config.MESSAGES['invalid_date'])
        return Config.DOB
    
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
            Config.MESSAGES['success'],
            reply_markup=get_main_keyboard()
        )
    else:
        update.message.reply_text(
            Config.MESSAGES['not_found'],
            reply_markup=get_main_keyboard()
        )
    
    context.user_data.clear()
    return Config.MAIN_MENU

# English: Mentor help handler
# Russian: Обработчик помощи ментора
def mentor_help(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        Config.MESSAGES['mentor_help'].format(mentor_username=Config.MENTOR_USERNAME),
        reply_markup=get_main_keyboard()
    )
    return Config.MAIN_MENU

# English: Cancel command handler
# Russian: Обработчик команды отмены
def cancel(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    update.message.reply_text(
        Config.MESSAGES['goodbye'],
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END 