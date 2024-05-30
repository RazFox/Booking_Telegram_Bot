from telebot.handler_backends import State, StatesGroup


class MyStates(StatesGroup):
    user_id = State()
    chat_user_id = State()
    is_bot = State()
    page_int = State()
    count_int = State()
    city_answer = State()
    city_id = State()
    search = State() # Флаг запуска поиска.
    start_day = State()
    start_month = State()
    start_age = State()
    finish_day = State()
    finish_month = State()
    finish_age = State()
    user_response_hotel = State()
