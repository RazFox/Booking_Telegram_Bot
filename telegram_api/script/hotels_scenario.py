"""Сценарий работы с отелями и номерами"""
from telebot.types import InlineKeyboardMarkup
from telebot import callback_data
from ..inline_board import Inline_keyboard_hotels
from site_api import rapid_api
from database import sqlite_db

inline_hotel = Inline_keyboard_hotels.Inline_board_hotel
api_site = rapid_api.Rapid_api()
SQL_lite = sqlite_db.SQLite_db_user()
SQL_lite_history = sqlite_db.SQLite_db_history()


def hotel_scenario(answer_call: str, user_id: int) -> [InlineKeyboardMarkup, str]:
    """
    Обрабатываем callback от пользователя и "меняем" страницы с отелями.
        :param answer_call: callback от пользователя.
        :param user_id: Пользователь
    :return:
    keyboard_inline: Объект с кнопками Inline.
    text_message: Текст сообщения для пользователя.
    """
    # Получаем данные из БД USER
    user_page = SQL_lite.search_user_db(user_id=user_id, user_column="page")
    user_count = SQL_lite.search_user_db(user_id=user_id, user_column="count")
    hotels_response = SQL_lite.search_user_db(user_id=user_id, user_column="user_response_hotel")
    # Обработка кнопки - вперед
    if answer_call == 'next-page':
        if user_page < user_count:
            user_page += 1
            SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="page", user_edit_data=user_page)
    # Обработка кнопки - назад
    elif answer_call == 'back-page':
        if user_page > 1:
            user_page -= 1
            SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="page", user_edit_data=user_page)
    keyboard_inline, text_message = inline_hotel.board_post_info(hotels=hotels_response,
                                                                 user_page=user_page, user_count=user_count)
    return keyboard_inline, text_message


def search_hotel(call_data: callback_data, user_id: int) -> [InlineKeyboardMarkup, str]:
    """
    Запрос на сайт hotels.com с указанными ранее пользователем параметрами.
        :param user_id: Пользователь
        :param call_data: Объект callback_data: хранит в себе callback пользователя.
    :return:
    keyboard_inline: Объект с кнопками Inline.
    text_message: Текст сообщения для пользователя.
    """
    sort = {"price": "PRICE_LOW_TO_HIGH", "star": "PROPERTY_CLASS", "ratio": "RECOMMENDED"}
    filter = {"price": {"price": {"max": 150, "min": 100}},
              "star": {"star": ["40", "50"]},
              "ratio": {"guestRating": "35"}}
    start_day = SQL_lite.search_user_db(user_id=user_id, user_column="start_day")
    start_month = SQL_lite.search_user_db(user_id=user_id, user_column="start_month")
    start_age = SQL_lite.search_user_db(user_id=user_id, user_column="start_age")
    finish_day = SQL_lite.search_user_db(user_id=user_id, user_column="finish_day")
    finish_month = SQL_lite.search_user_db(user_id=user_id, user_column="finish_month")
    finish_age = SQL_lite.search_user_db(user_id=user_id, user_column="finish_age")
    city_id = SQL_lite.search_user_db(user_id=user_id, user_column="city_id")
    rental_day = SQL_lite.search_user_db(user_id=user_id, user_column="user_rental_days")
    data_dict = {"start_day": start_day,
                 "start_month": start_month,
                 "start_year": start_age,
                 "finish_day": finish_day,
                 "finish_month": finish_month,
                 "finish_year": finish_age,
                 "sort_method": sort,
                 "filter_answer": filter
                 }
    method_sort = call_data.data.split("_")[1]
    response_hotel = api_site.resp_get_hotel(id_loc=city_id, data_user=data_dict)
    response_date = api_site.reade_response(hotel=response_hotel, user_rental_day=rental_day)
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_response_hotel",
                                         user_edit_data=response_date)
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="page", user_edit_data=1)
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="count", user_edit_data=len(response_date))
    keyboard_inline, text_message = hotel_scenario(answer_call=call_data, user_id=user_id)
    return keyboard_inline, text_message


def hotel_photo_scenario(user_id: int, id_hotels: str) -> [InlineKeyboardMarkup, str]:
    """
    Метод поиска информации по выбранному отелю с помощью ID отеля из callback ответа.
        :param user_id: ID пользователя
        :param id_hotels: ID отеля из callback ответа.
    :return:
    keyboard_inline - Объект с клавиатурой Inline.
    text_message - Сообщение пользователю.
    """
    response = api_site.hotels_info(int(id_hotels))
    user_page = 1
    response_data = api_site.read_response_hotel(response)
    user_count = len(response_data.get("image"))
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_image_count", user_edit_data=user_count)
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_image_page", user_edit_data=user_page)
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_hotel_image", user_edit_data=response_data)
    keyboard_inline, text_message = inline_hotel.board_hotels_info(hotel=response_data,
                                                                   user_page=user_page, user_count=user_count)
    return keyboard_inline, text_message


def hotel_keyboard_photo(user_id: int, answer_call: str) -> [InlineKeyboardMarkup, str]:
    """
    Метод создания сообщения и клавиатура с фотографиями отеля.
    Принимает и обрабатывает callback для переключения между фото.
        :param user_id: ID пользователя.
        :param answer_call: callback от пользователя в виде str
    :return:
    keyboard_inline - Объект с клавиатурой Inline.
    text_message - Сообщение пользователю.
    """
    user_page = SQL_lite.search_user_db(user_id=user_id, user_column="user_image_page")
    user_count = SQL_lite.search_user_db(user_id=user_id, user_column="user_image_count")
    user_hotel_photo = SQL_lite.search_user_db(user_id=user_id, user_column="user_hotel_image")

    if answer_call == 'next-page-image':
        if user_page < user_count:
            user_page += 1
            SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_image_page",
                                                 user_edit_data=user_page)
    # Обработка кнопки - назад
    elif answer_call == 'back-page-image':
        if user_page > 1:
            user_page -= 1
            SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_image_page",
                                                 user_edit_data=user_page)
    keyboard_inline, text_message = inline_hotel.board_hotels_info(hotel=eval(user_hotel_photo),
                                                                   user_page=user_page, user_count=user_count)
    return keyboard_inline, text_message


def hotel_history(user_id: int, answer_call: str):
    """
    Метод создания сообщения и клавиатура с фотографиями отеля.
    Принимает и обрабатывает callback для переключения между фото.
        :param user_id: ID пользователя.
        :param answer_call: callback от пользователя в виде str
    :return:
    keyboard_inline - Объект с клавиатурой Inline.
    text_message - Сообщение пользователю.
    """
    user_page_hist = SQL_lite.search_user_db(user_id=user_id, user_column="user_page_hist")
    user_hotel_photo_hist = SQL_lite_history.search_history_db(user_id=user_id)
    user_count_hist = len(user_hotel_photo_hist)
    SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_count_hist",
                                         user_edit_data=user_count_hist)

    if answer_call == 'next-page-history':
        if user_page_hist < user_count_hist:
            user_page_hist += 1
            SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_page_hist",
                                                 user_edit_data=user_page_hist)
    # Обработка кнопки - назад
    elif answer_call == 'back-page-history':
        if user_page_hist > 1:
            user_page_hist -= 1
            SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="user_page_hist",
                                                 user_edit_data=user_page_hist)
    keyboard_inline, text_message = inline_hotel.board_post_info_history(hotels=user_hotel_photo_hist,
                                                                         user_page=user_page_hist,
                                                                         user_count=user_count_hist)
    return keyboard_inline, text_message
