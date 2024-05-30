from ..inline_board import Inline_keyboard_hotels, mini_keyboard_inline, Inline_keyboard_start
from .hotels_scenario import hotel_scenario, search_hotel, hotel_photo_scenario, hotel_keyboard_photo, hotel_history
from .city_scenario import city_input, search_city
from .travel_date_scenario import calendar
from database import sqlite_db
from . import script_db_info

inline_hotel = Inline_keyboard_hotels.Inline_board_hotel
mini_inline = mini_keyboard_inline.Mini_Inline_KeyBoard
start_inline = Inline_keyboard_start.Inline_board_start
SQL_lite = sqlite_db.SQLite_db_user()
SQL_lite_history = sqlite_db.SQLite_db_history()


def answer(call):
    """
    Функция обрабатывает входящие callback от пользователя и запускает тот или иной сценарий.
        :param call: Объект callback - содержит в себе данные о том какую именно кнопку активировал пользователь.
        :return:
            keyboard_inline - Объект InlineKeyboardMarkup - содержит в себе объект inline-кнопок
            text_message - str - Содержит в себе текст сообщения для пользователя.
    """
    keyboard_inline, text_message = start_inline.error_menu()
    user_id = call.from_user.id
    answer_call = call.data.split('_')[0]
    if answer_call == 'search-hotel':
        # Запуск сценария поиска отеля. Вызов функции для ввода города.
        keyboard_inline, text_message = city_input(user_id)
    elif answer_call in ["next-page", 'back-page', 'price']:
        # Запуск сценария для работы с выгрузкой по отелям
        keyboard_inline, text_message = hotel_scenario(answer_call, user_id)
    elif answer_call == 'open-data':
        script_db_info.history_db_hotels(user_id=user_id)
        keyboard_inline, text_message = hotel_photo_scenario(user_id=user_id, id_hotels=call.data.split('_')[1])
    elif answer_call in ['next-page-image', 'back-page-image']:
        keyboard_inline, text_message = hotel_keyboard_photo(user_id=user_id, answer_call=answer_call)
    elif answer_call == 'exit-hotels':
        keyboard_inline, text_message = hotel_scenario(answer_call, user_id)
    elif answer_call in ['history-hotel', 'next-page-history', 'back-page-history']:
        keyboard_inline, text_message = hotel_history(user_id=user_id, answer_call=answer_call)
    elif answer_call in ["city", 'restart-date']:
        # Записываем пользователю id города/наименование города где ищется отель, и запускаем сценарий ввода дат.
        if answer_call == "city":
            SQL_lite.edit_data_for_db_user_table(user_id=user_id,
                                                 user_column="city_id", user_edit_data=call.data.split('_')[1])
        keyboard_inline, text_message = calendar(call, user_id)
    elif answer_call in ["starting-day", "starting-month", "starting-year", "final-year", "final-month", "final-day"]:
        # Работа с кнопками дат начала бронирования и конца бронирования.
        keyboard_inline, text_message = calendar(call, user_id)
    elif answer_call == "sort":
        # Поиск отеля и получения выгрузки по отелям.
        keyboard_inline, text_message = search_hotel(call, user_id)
    else:
        pass
    return keyboard_inline, text_message


def search_hotel_scenario(message, user_id):
    """
    Обрабатывает сообщение с городом от пользователя и запускает поиск данного города.
    :param user_id: Пользователь
    :param message: Сообщение от пользователя с названием города.
    :return:
        keyboard_inline: InlineKeyboardMarkup: Объект с кнопками Inline.
        text_message: str: Текст сообщения для пользователя.
    """
    keyboard_inline, text_message = search_city(message)
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="search", user_edit_data=0)
    return keyboard_inline, text_message
