from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class Inline_board_start:

    @classmethod
    def start_menu(cls) -> InlineKeyboardMarkup:
        """
        Основное меню с Inline_кнопками.
        Вызывается после команды /start
        :return:
        markup: Объект с Inline-кнопками.
        """
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f'Hotel Search', callback_data=f'search-hotel'))
        markup.add(InlineKeyboardButton(text=f'Hotel search history', callback_data=f'history-hotel'))
        return markup

    @classmethod
    def error_menu(cls):
        text_message = "It seems that you have some kind of error... :( We're sorry..."
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f'Start Over.', callback_data=f'restart'))
        markup.add(InlineKeyboardButton(text=f'Report a bug.', callback_data=f'error_report'))
        return markup, text_message