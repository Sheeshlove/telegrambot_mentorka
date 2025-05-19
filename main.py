from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from config.config import Config
from handlers.conversation import (
    start, main_menu, get_snils, get_fio, get_dob,
    check_user_data, mentor_help, cancel
)

# English: Main function to run the bot
# Russian: Главная функция для запуска бота
def main():
    # English: Initialize bot and dispatcher
    # Russian: Инициализация бота и диспетчера
    updater = Updater(Config.TOKEN)
    dispatcher = updater.dispatcher

    # English: Add conversation handler
    # Russian: Добавление обработчика разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            Config.MAIN_MENU: [
                MessageHandler(Filters.text & ~Filters.command, main_menu)
            ],
            Config.SNILS: [
                MessageHandler(Filters.text & ~Filters.command, get_snils)
            ],
            Config.FIO: [
                MessageHandler(Filters.text & ~Filters.command, get_fio)
            ],
            Config.DOB: [
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