from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Mini_Inline_KeyBoard:

    @classmethod
    def one_keyboard_inline(cls, text_button: str, callback_data: str) -> InlineKeyboardMarkup:
        """
        Возвращает объект InlineKeyboardMarkup с одной кнопкой inline
        :param text_button: Текст для кнопки Inline.
        :param callback_data: Данный для callback_кнопки.
        :return:
            one_inline: InlineKeyboardMarkup: Объект с Inline_кнопкой.
        """
        one_inline = InlineKeyboardMarkup()
        one_inline.add(InlineKeyboardButton(text=text_button, callback_data=callback_data))
        return one_inline

    @classmethod
    def generator_inline_keyboard(cls, text_data: dict, count_column: int, data_code: str) -> InlineKeyboardMarkup:
        """
        Функция генератор inline кнопок по заданным параметрам.
        :param text_data: Словарь содержащий в себе наименование кнопки и callback. {str: str}
        :param count_column: Количество столбцов в inline клавиатуре.
        :param data_code: callback код. Содержит в себе данные для определение в типа callback.
        :return:
            inline_keyboard_markup: InlineKeyboardMarkup: Объект с кнопками inline
        """
        buttons = list()
        button_row = list()

        for element_text, element_data in text_data.items():
            buttons.append(
                InlineKeyboardButton(text=element_text, callback_data="{}_{}".format(data_code, element_data)))
            if len(buttons) == count_column:
                button_row.append(buttons)
                buttons = list()
        button_row.append(buttons)
        inline_keyboard_markup = InlineKeyboardMarkup(keyboard=button_row)

        return inline_keyboard_markup

    @classmethod
    def edit_inline(cls, inline_keyboard, text, callback):
        """
        Функция для редактирования inline-клавиатуры, добавляет в нее 1 кнопкую на новую строку.
        """
        inline_keyboard.row(InlineKeyboardButton(text=text, callback_data=callback))
        return inline_keyboard