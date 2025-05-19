import os
from dotenv import load_dotenv

# English: Load environment variables
# Russian: Загрузка переменных окружения
load_dotenv()

# English: Bot configuration
# Russian: Конфигурация бота
class Config:
    # English: Bot token from environment variable
    # Russian: Токен бота из переменной окружения
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7223734470:AAGoQflInEfUz5APYflFb1BciDwyTqNK-II')
    
    # English: Mentor's username
    # Russian: Имя пользователя ментора
    MENTOR_USERNAME = '@sheeshlove'
    
    # English: Chat states
    # Russian: Состояния чата
    MAIN_MENU, SNILS, FIO, DOB = range(4)
    
    # English: Message templates
    # Russian: Шаблоны сообщений
    MESSAGES = {
        'welcome': (
            "👋 Привет! Я бот-помощник для первокурсников.\n\n"
            "Выберите нужный раздел:"
        ),
        'snils_format': (
            "Для доступа к чату первокурсников, пожалуйста, введите ваш СНИЛС\n"
            "Формат: XXX-XXX-XXX XX\n"
            "Например: 123-456-789 00"
        ),
        'invalid_snils': (
            "❌ Неверный формат СНИЛС!\n"
            "Пожалуйста, введите СНИЛС в формате: XXX-XXX-XXX XX\n"
            "Например: 123-456-789 00"
        ),
        'invalid_fio': (
            "❌ Пожалуйста, введите полное ФИО (Фамилия Имя Отчество)"
        ),
        'invalid_date': (
            "❌ Неверный формат даты!\n"
            "Пожалуйста, используйте формат: YYYY-MM-DD\n"
            "Например: 2000-01-01"
        ),
        'success': (
            "✅ Данные подтверждены!\n\n"
            "Ссылка на чат первокурсников: [будет добавлена позже]\n\n"
            "Для возврата в главное меню нажмите /start"
        ),
        'not_found': (
            "❌ К сожалению, ваши данные не найдены в базе.\n"
            "Пожалуйста, проверьте введенные данные и попробуйте снова.\n\n"
            "Для возврата в главное меню нажмите /start"
        ),
        'mentor_help': (
            "👨‍🏫 Для получения помощи от ментора, пожалуйста, напишите:\n"
            "{mentor_username}\n\n"
            "Для возврата в главное меню нажмите /start"
        ),
        'goodbye': (
            "До свидания! Для начала работы нажмите /start"
        )
    } 