"""Создание inline кнопок по отелям и номерам"""
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class Inline_board_hotel:

    @classmethod
    def board_post_info(cls, hotels: str, user_page: int, user_count: int) -> [InlineKeyboardMarkup, list]:
        """
        Функция создает шаблон сообщения пользователю с отелями:
        Наименование отеля, Общая цена, Цена за ночь, Рейтинг, Кол-во оценок и 1 фото отеля.
            :param hotels:
            :param user_page:
            :param user_count:
        :return:
        markup: Объект Inline клавиатуры.
        response_user_answer: Список из двух элементов, строка с сообщением пользователю и строка с ссылкой на изображение.
        """
        data_hotels = eval(hotels)
        info_hotel = data_hotels.get(user_page)
        response_text = cls.response_template(info_hotel)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f'<- Back', callback_data=f'back-page'),
                   InlineKeyboardButton(text=f'{user_page}/{user_count}', callback_data=f' '),
                   InlineKeyboardButton(text=f'Forward ->', callback_data=f'next-page'))
        markup.add(InlineKeyboardButton(text=f'More', callback_data='open-data_{}'.format(info_hotel["id"])))
        markup.add(InlineKeyboardButton(text=f'New search', callback_data='new_search-hotel'))
        response_user_answer = [response_text, info_hotel["photo_image"]]
        return markup, response_user_answer

    @classmethod
    def board_hotels_info(cls, hotel: dict, user_page: int, user_count: int) -> [InlineKeyboardMarkup, [str, str]]:
        """
        Подробная информация по отелю с фотографиями.
        Реализует клавиатуру для переключения между фото отеля.
            :param hotel: Словарь с данными по отелю.
            :param user_page: Страница пользователя из БД.
            :param user_count: Общее кол-во страниц из БД.
        :return:
        markup: Объект Inline клавиатуры
        response_user_answer: Список из двух элементов, строка с текстом сообщения и строка с ссылкой на изображение.
        """
        # TODO: Реализовать передачу в сообщение более подробной информации об отеле (особенности, нюансы, плюсы)
        image_hotel = hotel["image"]
        image = image_hotel[user_page]

        text_message = "Наименование отеля: {name}".format(name=hotel["name"])
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f'<- Back', callback_data=f'back-page-image'),
                   InlineKeyboardButton(text=f'{user_page}/{user_count}', callback_data=f' '),
                   InlineKeyboardButton(text=f'Forward ->', callback_data=f'next-page-image'))
        markup.add(InlineKeyboardButton(text=f'Back to hotels', callback_data='exit-hotels'))
        markup.add(InlineKeyboardButton(text=f'Open site', callback_data='open-url_{}'.format("None")))
        markup.add(InlineKeyboardButton(text=f'New search', callback_data='new_search-hotel'))
        response_user_answer = [text_message, image]
        return markup, response_user_answer

    @classmethod
    def board_post_info_history(cls, hotels: dict, user_page: int, user_count: int) -> [InlineKeyboardMarkup,
                                                                                       [str, str]]:
        """
        Функция создает шаблон сообщения пользователю с отелями из истории.
        Наименование отеля, Общая цена, Цена за ночь, Рейтинг, Кол-во оценок и 1 фото отеля.
            :param hotels:
            :param user_page:
            :param user_count:
        :return:
        markup: Объект inline клавиатуры
        response_user_answer: Объект списка из двух элементов, сообщение пользователю и ссылка на изображение.
        """
        info_hotel = hotels.get(user_page)
        response_text = cls.response_template(info_hotel)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text=f'<- Back', callback_data=f'back-page-history'),
                   InlineKeyboardButton(text=f'{user_page}/{user_count}', callback_data=f' '),
                   InlineKeyboardButton(text=f'Forward ->', callback_data=f'next-page-history'))
        markup.add(InlineKeyboardButton(text=f'More', callback_data='open-data_{}'.format(info_hotel["id"])))
        markup.add(InlineKeyboardButton(text=f'New search', callback_data='new_search-hotel'))
        response_user_answer = [response_text, info_hotel["photo_image"]]
        return markup, response_user_answer

    @classmethod
    def response_template(cls, info_hotel):
        response_template = "Наименование отеля: {name}\nОбщая цена: {price_total}" \
                            "\nЦена за ночь: {price_night}\n" \
                            "Рейтинг: {reviews} Кол-во оценок: {reviews_total}\n".format(name=info_hotel["name"],
                                                                                         price_total=info_hotel[
                                                                                             "price_total"],
                                                                                         price_night=info_hotel[
                                                                                             "price_night"],
                                                                                         reviews=info_hotel["reviews"][
                                                                                             "score"],
                                                                                         reviews_total=
                                                                                         info_hotel["reviews"]["total"])
        return response_template