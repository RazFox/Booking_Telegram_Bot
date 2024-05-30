"""Получение всех настроек, токены и ключи для работы с API"""

if __name__ != "__main__":
    import os
    from dotenv import load_dotenv, find_dotenv

    if not find_dotenv():
        exit("Error - Отсутствуют данные в файле.env")
    else:
        load_dotenv()

    TG_TOKEN = os.getenv("TG_TOKEN")
    RAPID_API_KEY = os.getenv("RAPID_API_KEY")
    RAPID_API_HOST = os.getenv("RAPID_API_HOST")

