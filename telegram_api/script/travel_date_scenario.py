from ..inline_board import Inline_keyboard_date, Inline_keyboard_sort, mini_keyboard_inline
from telebot.types import InlineKeyboardMarkup
from database import sqlite_db
import datetime

inline_calendar = Inline_keyboard_date.Inline_board_date
inline_sort = Inline_keyboard_sort.Sort_Inline_KeyBoard
SQL_lite = sqlite_db.SQLite_db_user()


def calendar(answer, user_id: int) -> [InlineKeyboardMarkup, str]:
    """
    Функция обрабатывает принятый callback по сценарию с датами.
    Определяется тип callback и возвращаются нужное сообщение и Inline_KeyBoard

    :param answer: объект Call от callback_query
    :param user_id: Пользователь
    :return:
        keyboard_inline: InlineKeyboardMarkup: Объект с кнопками Inline.
        text_message: str: Текст сообщения для пользователя.
    """
    answer_call = answer.data.split('_')[0]  # Получаем "тип" callback от пользователя и проверяем его в if
    answer_data = answer.data.split('_')[1]  # Получаем "данные" сохраненные в callback от пользователя.
    if answer_call in ["city", "restart-date"]:
        # Пользователь выбрал город из списка, возвращаем inline с годами начала бронирования.
        text_message = "Please indicate the start date of the booking:"
        keyboard_inline = inline_calendar.calendar_age("starting-year")

    elif answer_call == "starting-year":
        # Пользователь выбрал год начала брони из списка, возвращаем inline с месяцами начала бронирования.
        text_message = "Specify the start month of the booking:"
        SQL_lite.edit_data_for_db_user_table(user_column="start_age", user_edit_data=int(answer_data), user_id=user_id)
        keyboard_inline = inline_calendar.calendar_mount("starting-month", year=int(answer_data))

    elif answer_call == "starting-month":
        # Пользователь выбрал месяц начала брони из списка, возвращаем inline с днями начала бронирования.
        text_message = "Specify the start date of the booking:"
        SQL_lite.edit_data_for_db_user_table(user_column="start_month", user_edit_data=int(answer_data),
                                             user_id=user_id)
        start_age: [int] = SQL_lite.search_user_db(user_id=user_id, user_column="start_age")
        keyboard_inline = inline_calendar.calendar_day(int(answer_data), "starting-day", start_age)

    elif answer_call == "starting-day":
        # Пользователь выбрал день начала брони из списка, возвращаем inline с годами окончания бронирования.
        text_message = "Specify the end year of the booking:"
        SQL_lite.edit_data_for_db_user_table(user_id=user_id, user_column="start_day", user_edit_data=int(answer_data))
        keyboard_inline = inline_calendar.calendar_age("final-year")

    elif answer_call == "final-year":
        # Пользователь выбрал год окончания брони из списка, возвращаем inline с месяцами окончания бронирования.
        text_message = "Specify the end month of the booking:"
        SQL_lite.edit_data_for_db_user_table(user_column="finish_age", user_edit_data=int(answer_data), user_id=user_id)
        keyboard_inline = inline_calendar.calendar_mount("final-month", year=int(answer_data))

    elif answer_call == "final-month":
        # Пользователь выбрал месяц окончания брони из списка, возвращаем inline с днями окончания бронирования.
        text_message = "Specify the end date of the reservation:"
        SQL_lite.edit_data_for_db_user_table(user_column="finish_month", user_edit_data=int(answer_data),
                                             user_id=user_id)
        finish_age: [int] = SQL_lite.search_user_db(user_id=user_id, user_column="finish_age")
        keyboard_inline = inline_calendar.calendar_day(int(answer_data), "final-day", finish_age)

    elif answer_call == "final-day":
        # Пользователь выбрал день окончания брони из списка, возвращаем inline со способами сортировки отелей.
        SQL_lite.edit_data_for_db_user_table(user_column="finish_day", user_edit_data=int(answer_data), user_id=user_id)
        keyboard_inline, text_message = inline_sort.var_sort()
        if date_r(user_id=user_id):
            text_message = "Check-out date is less than check-in date!"
            keyboard_inline = mini_keyboard_inline.Mini_Inline_KeyBoard.one_keyboard_inline(
                text_button="Enter date again",
                callback_data="restart-date_1")
    return keyboard_inline, text_message


def date_r(user_id):
    """
    Функция проверяет данные веденные пользователем по дате заселения и выезда из отеля.
    Если дата заезда больше чем дата выезда, то выводится сообщение об некорректно веденных датах.
    """
    DT = datetime
    day_start = SQL_lite.search_user_db(user_id=user_id, user_column="start_day")
    month_start = SQL_lite.search_user_db(user_id=user_id, user_column="start_month")
    year_start = SQL_lite.search_user_db(user_id=user_id, user_column="start_age")
    day_finish = SQL_lite.search_user_db(user_id=user_id, user_column="finish_day")
    month_finish = SQL_lite.search_user_db(user_id=user_id, user_column="finish_month")
    year_finish = SQL_lite.search_user_db(user_id=user_id, user_column="finish_age")
    dt_start = DT.date(day=day_start, month=month_start, year=year_start)
    dt_finish = DT.date(day=day_finish, month=month_finish, year=year_finish)
    if dt_start > dt_finish:
        return True
    else:
        difference_date = dt_finish - dt_start
        count_rental_days = difference_date.days
        SQL_lite.edit_data_for_db_user_table(user_column="user_rental_days", user_edit_data=count_rental_days,
                                             user_id=user_id)
        return False
