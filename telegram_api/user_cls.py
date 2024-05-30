
class User_TG:
    """User_TG - временный класс пользователя для тестов"""

    def __init__(self, user_id: int, chat_user_id: int) -> None:
        """
        :param user_id: int - id пользователя
        :param chat_user_id: - id чата
        :param is_bot: bool - Проверка является ли пользователь юзер-ботом.
        """
        self.__user_id = user_id
        self.__chat_user_id = chat_user_id
        self.__is_bot = None
        self.__page_int = None
        self.__count_int = None
        self.__city_answer = None
        self.__city_id = None
        self.search = False
        self.__start_day = None
        self.__start_month = None
        self.__start_age = None
        self.__finish_day = None
        self.__finish_month = None
        self.__finish_age = None
        self.__user_response_hotel = None

    def get_user_id(self) -> int:
        return self.__user_id

    def get_chat_user_id(self) -> int:
        return self.__chat_user_id

    def get_is_bot(self) -> int:
        return self.__is_bot

    def get_page_int(self):
        return self.__page_int

    def get_count_int(self):
        return self.__count_int

    def get_city_answer(self):
        return self.__city_answer

    def get_city_id(self):
        return self.__city_id

    def get_user_response_hotel(self):
        return self.__user_response_hotel

    def get_start_age(self):
        return self.__start_age

    def get_finish_age(self):
        return self.__finish_age

    def set_page_int(self, set_int, check_init: bool = False):
        """Передаем параметр True когда нужно задать параметр страницы.
        Для изменения(перелистывания) страницы не указываем"""
        if check_init:
            self.__page_int = set_int
        else:
            self.__page_int += set_int

    def set_count_int(self, set_int):
        self.__count_int = set_int

    def set_city_answer_id(self, city):
        """Выбранный город пользователем"""
        self.__city_answer = city.split("+")[0]
        self.__city_id = city.split("+")[1]

    def set_start_day(self, day: str):
        self.__start_day = int(day)

    def set_start_month(self, month: str):
        self.__start_month = int(month)

    def set_start_age(self, age: str):
        self.__start_age = int(age)

    def set_finish_day(self, day: str):
        self.__finish_day = int(day)

    def set_finish_month(self, month: str):
        self.__finish_month = int(month)

    def set_finish_age(self, age: str):
        self.__finish_age = int(age)

    def set_user_response_hotel(self, response):
        self.__user_response_hotel = response

    def data(self):
        data_dict = {"start_day": self.__start_day,
                     "start_month": self.__start_month,
                     "start_year": self.__start_age,
                     "finish_day": self.__finish_day,
                     "finish_month": self.__finish_month,
                     "finish_year": self.__finish_age
                     }
        return data_dict

    def reset(self):
        """Обнуляет ряд атрибутов класса user"""
        pass


