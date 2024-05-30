from telebot.types import InlineKeyboardMarkup
from ..inline_board import mini_keyboard_inline
from site_api import rapid_api
from database import sqlite_db

inline_keyboard = mini_keyboard_inline.Mini_Inline_KeyBoard
SQL_lite = sqlite_db.SQLite_db_user()


def city_input(user_id) -> [InlineKeyboardMarkup, str]:
    """
    Функция возвращает пользователю сообщение и активирует флаг на прием текста от пользователя.
        :param user_id: ID пользователя
    :return:
    search_board: Объект inline-кнопок.
    text_message: Текст сообщения пользователю.
    """
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="search", user_edit_data=True)
    search_board = inline_keyboard.one_keyboard_inline("Request History", "history-hotel")
    text_message = "Enter the name of the city to search.\n" \
                   "Attention! The service does not work on the territory of the Russian Federation!"
    return search_board, text_message


def search_city(message) -> [InlineKeyboardMarkup, str]:
    """
    Ищем информацию по городу, полученному от пользователя и
    отправляем пользователю несколько городов на выбор для уточнения.
        :param message: Город переданный пользователем текстом в сообщение.
    :return:
    city_board: Объект inline-кнопок с перечислением ряда городов.
    text_message: Содержит в себе текст сообщения для пользователя.
    """
    rap = rapid_api.Rapid_api()
    data_hotels = rap.resp_search(city=message, locale="en_US")
    if isinstance(data_hotels, str):
        pass
    else:
        cities = dict()
        for elements in data_hotels["sr"]:
            if elements["type"] == "CITY":
                name = "{}, {}".format(elements["regionNames"]["shortName"],
                                       elements["regionNames"]["secondaryDisplayName"])
                id = elements["essId"]["sourceId"]
                text_name = "{}+{}".format(name, id)
                cities.update({name: id})
            else:
                pass
        city_board = inline_keyboard.generator_inline_keyboard(text_data=cities, count_column=2, data_code="city")
        keyboard_city = inline_keyboard.edit_inline(inline_keyboard=city_board,
                                                    callback="search-hotel", text="Enter the city again")
        text_message = "Select the desired city from the list:"
        return keyboard_city, text_message
