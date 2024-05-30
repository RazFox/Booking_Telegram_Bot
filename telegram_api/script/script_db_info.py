from database import sqlite_db

SQLite_user = sqlite_db.SQLite_db_user()
SQLite_history = sqlite_db.SQLite_db_history()

def history_db_hotels(user_id: int) -> None:
    """
    Функция записывает данные в бд History. История пользователя по отелям.
    Записывает те отели, где пользователь нажал кнопку "Подробнее".
        :param user_id: ID пользователя
    :return: None
    """
    user_hotel_response = SQLite_user.search_user_db(user_id=user_id, user_column="user_response_hotel")
    user_page = SQLite_user.search_user_db(user_id=user_id, user_column="page")
    user_table_response = eval(user_hotel_response)
    user_hotel = user_table_response.get(user_page)
    SQLite_history.create_db_history_info(user_id=user_id, user_response=user_hotel)
