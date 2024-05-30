import datetime
from telebot.types import InlineKeyboardMarkup
from ..inline_board import mini_keyboard_inline

mini_inline = mini_keyboard_inline.Mini_Inline_KeyBoard


class Inline_board_date():

    @classmethod
    def calendar_day(cls, mount: int, callback_data: str, user_answer_age: int) -> InlineKeyboardMarkup:
        """
        Метод для создания inline объекта кнопок календарного месяца по дням.
            :param mount: номер месяца выбранный пользователем.
            :param callback_data: данный для callback_кнопок.
            :param user_answer_age: данные от пользователя по выбранному году.
        :return:
        builder_calendar_day: Объект кнопок Inline в виде календарного месяца от 1 до N.
        """
        date = datetime.date.today()
        if date.month == mount:
            start_day = date.day
        else:
            start_day = 1
        if mount in [1, 3, 5, 8, 10, 12]:
            range_day_end = 32
        elif mount == 2:
            # Проверка на високосный год при выборе февраля.
            if user_answer_age % 4 == 0:
                range_day_end = 30
            else:
                range_day_end = 29
        else:
            range_day_end = 31
        month_day_calendar = dict()
        for day in range(start_day, range_day_end):
            month_day_calendar.update({day: day})
        builder_calendar_day = mini_inline.generator_inline_keyboard(text_data=month_day_calendar,
                                                                     count_column=7, data_code=callback_data)
        return builder_calendar_day

    @classmethod
    def calendar_mount(cls, callback_data: str, year: int) -> InlineKeyboardMarkup:
        """
        Метод для создания inline объекта кнопок года в разрезе месяцов.
        :param callback_data: данный для callback_кнопок.
        :return:
            builder_calendar_month -> Объект InlineKeyboardMarkup: кнопки в разрезе месяцев Январь...Декабрь.
        """

        month_info = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                      "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
        date = datetime.date.today()
        #  Проверка, если пользователь выбрал текущий год, то месяца начнутся с текущего месяца.
        if date.year == year:
            new_month_info = dict()
            start_mount = date.month
            for mount_name, number in month_info.items():
                if start_mount > number:
                    pass
                else:
                    new_month_info.update({mount_name: number})
        else:
            new_month_info = month_info

        builder_calendar_month = mini_inline.generator_inline_keyboard(text_data=new_month_info,
                                                                       count_column=3, data_code=callback_data)
        return builder_calendar_month

    @classmethod
    def calendar_age(cls, callback_data: str) -> InlineKeyboardMarkup:
        """
        Метод для создания inline объекта кнопок годов.
        :param callback_data: данный для callback_кнопок.
        :return:
            builder_calendar_age -> Объект InlineKeyboardMarkup: кнопки с двумя годами(Текущим и следующим)
        """
        day, month, age = datetime.datetime.strftime(datetime.date.today(), "%d/%m/%Y").split("/")
        age_keyboard = dict()
        for age_insert in range(int(age), int(age) + 2):
            age_keyboard.update({age_insert: age_insert})
        builder_calendar_age = mini_inline.generator_inline_keyboard(text_data=age_keyboard,
                                                                     count_column=2, data_code=callback_data)
        return builder_calendar_age
