from peewee import *


class SQLite_db_user():

    def __init__(self):
        self.User_db = self.create_data_base()

    def create_data_base(self):
        """Функция должна проверять наличие базы данных, при ее отсутствие, создавать таблицы в БД"""
        self.db_user = SqliteDatabase("User.db", pragmas={'journal_mode': 'wal'})

        class BaseModel(Model):
            class Meta:
                database = self.db_user

        class User(BaseModel):
            user_id = IntegerField()
            chat_user_id = IntegerField()
            page = IntegerField()
            count = IntegerField()
            city_id = CharField()
            search = IntegerField()
            start_day = IntegerField()
            start_month = IntegerField()
            start_age = IntegerField()
            finish_day = IntegerField()
            finish_month = IntegerField()
            finish_age = IntegerField()
            user_rental_days = IntegerField()
            user_response_hotel = CharField()
            user_image_page = IntegerField()
            user_image_count = IntegerField()
            user_hotel_image = CharField()
            user_page_hist = IntegerField()
            user_count_hist = IntegerField()

        # TODO: Продумать проверку на наличие таблицы, если таблица отсутствует - создать.
        User.create_table()

        return User

    def search_user_db(self, user_column: str, user_id: int) -> any:
        """
        Метод для получения данных из БД User.
            :param user_column: Наименование столбца в таблице базы данных.
            :param user_id: ID пользователя в сервисе телеграмм
            :return answer_data_user: - данные из БД
        """
        with self.db_user:
            User = self.User_db
            database_info = {"user_id": User.get(User.user_id == user_id).user_id,
                             "chat_user_id": User.get(User.user_id == user_id).chat_user_id,
                             "page": User.get(User.user_id == user_id).page,
                             "count": User.get(User.user_id == user_id).count,
                             "city_id": User.get(User.user_id == user_id).city_id,
                             "search": User.get(User.user_id == user_id).search,
                             "start_day": User.get(User.user_id == user_id).start_day,
                             "start_month": User.get(User.user_id == user_id).start_month,
                             "start_age": User.get(User.user_id == user_id).start_age,
                             "finish_day": User.get(User.user_id == user_id).finish_day,
                             "finish_month": User.get(User.user_id == user_id).finish_month,
                             "finish_age": User.get(User.user_id == user_id).finish_age,
                             "user_response_hotel": User.get(User.user_id == user_id).user_response_hotel,
                             "user_image_page": User.get(User.user_id == user_id).user_image_page,
                             "user_image_count": User.get(User.user_id == user_id).user_image_count,
                             "user_hotel_image": User.get(User.user_id == user_id).user_hotel_image,
                             "user_rental_days": User.get(User.user_id == user_id).user_rental_days,
                             "user_page_hist": User.get(User.user_id == user_id).user_page_hist,
                             "user_count_hist": User.get(User.user_id == user_id).user_count_hist
                             }
            answer_data_user = database_info.get(user_column)
        return answer_data_user


    def create_db_user_info(self, user_id: int) -> None:
        """
        Метод для добавления нового пользователя в бд User.
        Если пользователь уже есть в БД, то пропускает этот шаг.
            :param user_id: ID пользователя в телеграмме.
        """
        User = self.User_db
        if User.get_or_none(user_id=user_id) is None:
            with self.db_user:
                User.create(user_id=user_id, chat_user_id=1, page=1, count=1, city_id=1, search=0,
                            start_day=1, start_month=1, start_age=1, finish_day=1, finish_month=1, finish_age=1,
                            user_response_hotel=1, user_image_page=1, user_image_count=1, user_hotel_image="null",
                            user_rental_days=1, user_page_hist=1, user_count_hist=1)

    def edit_data_for_db_user_table(self, user_column: str, user_edit_data: any, user_id: int) -> None:
        """
        Метод для редактирования данных в таблице User с данными от пользователя.
            :param user_edit_data: Пользовательские данные для записи в таблицу.
            :param user_id: ID пользователя которые нужно изменить в таблице.
            :param user_column: Наименование столбца в таблице которое нужно изменить.
                user_id: int - ID пользователя в сети telegram
                chat_user_id: int - ID чата с пользователе в telegram
                page: int - Номер страницы на которой находится пользователь
                count: int - Количество всего страниц в данных по отелям
                city_id: int - ID города на сайте hotels.com
                search: str - Хранит в себе bool значение True или False о флаге запуска поиска пользователем.
                start_day: int - Стартовая дата начала бронирования отеля
                start_month: int - Стартовый месяц начала бронирования отеля
                start_age: int - Стартовый год начала бронирования отеля
                finish_day: int - Конечная дата окончания бронирования отеля
                finish_month: int - Конечный месяц окончания бронирования отеля
                finish_age: int - Конечный год окончания бронирования отеля)
                user_response_hotel: str - Хранит в себе ответ от сервера пользователю с отелями в формате словаря dict
                user_image_page: int - Страница с фотографиями
                user_image_count: int - Всего страниц с фото(удалить?)
                user_hotel_image: str - данные по фотографиям отеля в формате dict
                user_rental_days: int - Длительность аренды номера пользователем
                user_page_hist: int - Номер страницы в History
                user_count_hist: int - Кол-во страниц(записей в БД History)
        """
        User = self.User_db
        database_info = {"user_id": {User.user_id: user_edit_data},
                         "chat_user_id": {User.chat_user_id: user_edit_data},
                         "page": {User.page: user_edit_data},
                         "count": {User.count: user_edit_data},
                         "city_id": {User.city_id: user_edit_data},
                         "search": {User.search: user_edit_data},
                         "start_day": {User.start_day: user_edit_data},
                         "start_month": {User.start_month: user_edit_data},
                         "start_age": {User.start_age: user_edit_data},
                         "finish_day": {User.finish_day: user_edit_data},
                         "finish_month": {User.finish_month: user_edit_data},
                         "finish_age": {User.finish_age: user_edit_data},
                         "user_response_hotel": {User.user_response_hotel: user_edit_data},
                         "user_image_page": {User.user_image_page: user_edit_data},
                         "user_image_count": {User.user_image_count: user_edit_data},
                         "user_hotel_image": {User.user_hotel_image: user_edit_data},
                         "user_page_hist": {User.user_page_hist: user_edit_data},
                         "user_count_hist": {User.user_count_hist: user_edit_data},
                         "user_rental_days": {User.user_rental_days: user_edit_data}
                         }
        with self.db_user:
            method_edit_column = database_info.get(user_column)
            User.update(method_edit_column).where(User.user_id == user_id).execute()


class SQLite_db_history:

    def __init__(self):
        self.History_db = self.create_data_base()

    def create_data_base(self):
        """Функция должна проверять наличие базы данных, при ее отсутствие, создавать таблицы в БД"""
        self.db_history = SqliteDatabase("History.db", pragmas={'journal_mode': 'wal'})

        class BaseModel(Model):
            class Meta:
                database = self.db_history

        class History(BaseModel):
            user_id = IntegerField()
            user_response = CharField()

        # TODO: Продумать проверку на наличие таблицы, если таблица отсутствует - создать.
        History.create_table()

        return History

    def search_history_db(self, user_id: int) -> dict:
        """
        Метод для получения данных из БД History.
            :param user_id: ID пользователя в сервисе телеграмм
            :return response_data: - данные из БД
        """
        History = self.History_db
        response_data = dict()
        with self.db_history:
            for number_id, response in enumerate(History.select().where(History.user_id == user_id)):
                response_data.update({number_id + 1: eval(response.user_response)})
        return response_data

    def create_db_history_info(self, user_id: int, user_response: dict) -> None:
        """
        Метод для добавления истории поиска для пользователя.
        Если в таблице у пользователя уже имеется 10 записей, удаляет более старую и записывает новую,
        если записей менее 10, то просто записывает новую строку.
            :param user_id: ID пользователя в телеграмме.
            :param user_response: информация об отеле по запросу пользователя
        """
        History = self.History_db
        response_data = list()
        with self.db_history:
            for response in History.select().where(History.user_id == user_id):
                response_data.append(response.id)
        if len(response_data) == 10:
            History.delete_by_id(response_data[0])
        History.create(user_id=user_id, user_response=user_response)



