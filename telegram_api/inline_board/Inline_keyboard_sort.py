from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Sort_Inline_KeyBoard:


    @classmethod
    def var_sort(cls) -> [InlineKeyboardMarkup, str]:
        """
        Функция создания Inline-кнопок для выбора пользователем принципа сортировки выборки.
        :return:
        key_sort_inline: Объект с кнопками Inline.
        sort_text: Текст сообщения для пользователя.
        """
        sort_text = "Choose a sorting method:"
        key_sort_inline = InlineKeyboardMarkup()
        key_sort_inline.add(InlineKeyboardButton(text="By price", callback_data="sort_price"),
                            InlineKeyboardButton(text="By rating", callback_data="sort_ratio"))
        key_sort_inline.add(InlineKeyboardButton(text="By star", callback_data="sort_star"))

        return key_sort_inline, sort_text
