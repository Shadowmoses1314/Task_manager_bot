import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from parse_json import parse_json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
# Получение Chat ID менеджера из переменной окружения
manager_chat_id = os.getenv('MANAGER_CHAT_ID')


def start(update: Update, context):
    # представим что здесь мы делаем запрос к гугл GoogleSheet, и получаем json файл с задачами
    json_str = "reminders.json"
    data = parse_json(json_str)

    # допилить чтобы принимать много 
    if data is not None:
        tel_id = data["tel_id"]
        task = data["task"]
        date = data["date"] # реалтзовать проверку даты
        time = data["time"] # реалтзовать проверку времени
        time_answer = data["time_answer"]

    chat_id = str(update.effective_chat.id)

    if tel_id == chat_id:

        keyboard = [
            [InlineKeyboardButton('Выполнено', callback_data='done')],
            [InlineKeyboardButton('Невыполнено', callback_data='not_done')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = context.bot.send_message(chat_id=chat_id,
                                           text=f'Task: {task}',
                                           reply_markup=reply_markup)

        context.job_queue.run_once(callback_not_answered, int(time_answer),
                                   context=(chat_id, message.message_id))
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text='Ошибка: Не соответствующий идентификатор пользователя'
            )


def button_callback(update, context):
    query = update.callback_query
    choice = query.data

    context.job_queue.stop()

    if choice == 'done':
        query.answer(text="Вы выбрали 'Выполнено'")
    elif choice == 'not_done':
        query.answer(text="Вы выбрали 'Невыполнено'")

    context.bot.send_message(chat_id=manager_chat_id,
                             text=f'Пользователь выбрал: {choice}')


def callback_not_answered(context):
    chat_id, message_id = context.job.context

    context.bot.delete_message(chat_id=chat_id, message_id=message_id)

    context.bot.send_message(chat_id=manager_chat_id,
                             text='Пользователь не ответил вовремя')


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)

    button_callback_handler = CallbackQueryHandler(button_callback)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(button_callback_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
