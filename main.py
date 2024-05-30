import telebot
from settings import settings
from telegram_api.script import callback_scenario
from telegram_api import inline_board
from database import sqlite_db

bot = telebot.TeleBot(settings.TG_TOKEN)

# Inline
inline_start = inline_board.Inline_keyboard_start.Inline_board_start()

# Scenario-Script
callback_scenario = callback_scenario

SQL_User = sqlite_db.SQLite_db_user()
SQL_lite_history = sqlite_db.SQLite_db_history()


@bot.message_handler(commands=['start'])
def start(message):
    """
    Обработка команды /start.
    Инициализирует работу с ботом.
    :param message: Сообщение от пользователя с командой start
    :return: None
    """
    #  Приветствуем пользователя
    if message.from_user.id in []:
        pass
    else:
        text_hello = "Hello {} {}! We are glad to welcome you in the chat for the selection of hotels! " \
                     "Click 'Search Hotels' and I'll help you find the best option!".\
            format(message.from_user.first_name, message.from_user.last_name)
        SQL_User.create_data_base()
        SQL_User.create_db_user_info(user_id=message.from_user.id)
        SQL_lite_history.create_data_base()
        keyboard_inline_start = inline_start.start_menu()
        bot.send_message(message.from_user.id, text_hello, reply_markup=keyboard_inline_start)


@bot.callback_query_handler(func=lambda call: call.data == "new_search-hotel")
def callback_query(call):
    """
    Обработка callback с запуском нового поиска отелей.
    """
    text_hello = "Hello {} {}! We are glad to welcome you in the chat for the selection of hotels! " \
                 "Click 'Search Hotels' and I'll help you find the best option!".\
        format(call.from_user.first_name, call.from_user.last_name)
    SQL_User.create_data_base()
    SQL_User.create_db_user_info(user_id=call.from_user.id)
    SQL_lite_history.create_data_base()
    keyboard_inline_start = inline_start.start_menu()
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    bot.send_message(call.from_user.id, text_hello, reply_markup=keyboard_inline_start)


@bot.callback_query_handler(func=lambda call: call.data == " ")
def callback_query():
    """
    Обработка пустого callback от пользователя.
    """
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Обработка callback запросов от кнопок inline.
    Инициализирует сценарий проверки сообщения в callback.
    :param call: Объект callback - Ответ пользователя на inline_кнопки.
    :return: None
    """
    keyboard_inline, text = callback_scenario.answer(call)
    if isinstance(text, list):
        text_message, image = text
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(chat_id=call.message.chat.id, photo=image, reply_markup=keyboard_inline, caption=text_message)
    else:
        bot.edit_message_text(text, reply_markup=keyboard_inline, chat_id=call.message.chat.id,
                              message_id=call.message.message_id)


@bot.message_handler(content_types=['text'])
def message_text(message):
    """
    Обработка входящего текст от пользователя для получения города. Флаг user.search == True
    Если флаг False, то проигнорирует сообщение от пользователя.
    :param message: Сообщение от пользователя.
    :return: None
    """
    user_id = message.from_user.id
    user_flag_search = SQL_User.search_user_db(user_id=user_id, user_column="search")
    if user_flag_search == 1:  # Проверяем что флаг сбора данных от пользователя активен.
        keyboard_inline, text = callback_scenario.search_hotel_scenario(message.text, user_id)
        bot.send_message(message.from_user.id, text, reply_markup=keyboard_inline)
    else:
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
