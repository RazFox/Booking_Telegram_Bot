"""Работа с API сайта Rapid_API по сайту hotels.com
Rapid_API Hotels - https://rapidapi.com/apidojo/api/hotels4/
Сайт Hotels - https://www.hotels.com/?locale=en_IE&pos=HCOM_EMEA&siteid=300000025
"""
import requests
from settings import settings
from database import sqlite_db

SQLite_user = sqlite_db.SQLite_db_user()

class Rapid_api:

    def __init__(self):
        self.__url_search = "https://hotels4.p.rapidapi.com/locations/v3/search"
        self.__url_properties = "https://hotels4.p.rapidapi.com/properties/v2/list"
        self.__url_properties_detail = "https://hotels4.p.rapidapi.com/properties/v2/detail"
        self.__headers = {
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": settings.RAPID_API_HOST
        }
        self.error_message = "Обнаружена ошибка!"

    def response_api(self, method_request: str, url: str, headers: dict, params: dict):
        response = requests.request(method_request, url, headers=headers, params=params)

        if response.ok:
            data = response.json()
            return data
        else:
            return self.error_message

    def resp_search(self, city: str, locale: str) -> requests:
        """
        Метод запроса информации по городу
        :param city: Город принятый от пользователя
        :param locale: Локаль
        :return:
            city_data: JSON: Данные по локациям с сайта hotels.com
        """
        querystring = {"q": city, "locale": locale, "langid": "1033", "siteid": "300000001"}
        response = requests.request("GET", self.__url_search, headers=self.__headers, params=querystring)

        if response.ok:
            city_data = response.json()
            return city_data
        else:
            return self.error_message

    def resp_get_hotel(self, id_loc: str, data_user: dict):
        """
        Endpoint - properties/v2/list
        Поиск по ID геолокации, с параметрами.

        :param id_loc: ID локации/города сайта hotels.com
        :param sort_method: Метод сортировки
        :param data_user: Даты начала и окончания бронирования {str: int}
        :return:
            hotel_data: JSON: Данные в формате json по отелям.
        """
        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "destination": {"regionId": id_loc},
            "checkInDate": {
                "day": data_user["start_day"],
                "month": data_user["start_month"],
                "year": data_user["start_year"]
            },
            "checkOutDate": {
                "day": data_user["finish_day"],
                "month": data_user["finish_month"],
                "year": data_user["finish_year"]
            },
            "rooms": [
                {
                    "adults": 1,
                    "children": []
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": 50,
            "sort": data_user["sort_method"],
            "filters": data_user["filter_answer"]
        }
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": settings.RAPID_API_HOST
        }
        response = requests.request("POST", self.__url_properties, json=payload, headers=headers)

        if response.ok:
            hotel_data = response.json()
            return hotel_data
        else:
            print("Error")

    def hotels_info(self, id_hotels: int):
        """
        Делает запрос по ID отеля, для получения подробной информации.
        """

        payload = {
            "currency": "USD",
            "eapid": 1,
            "locale": "en_US",
            "siteId": 300000001,
            "propertyId": "{}".format(id_hotels)
        }

        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": settings.RAPID_API_KEY,
            "X-RapidAPI-Host": settings.RAPID_API_HOST
        }

        response = requests.request("POST", self.__url_properties_detail, json=payload, headers=headers)

        if response.ok:
            hotel_data_info = response.json()
            return hotel_data_info
        else:
            print("Error")

    def reade_response(self, hotel: dict, user_rental_day: int):
        """
        Обрабатывает запрос от сайта по отелям и составляет словарь с отелями по определенным ключам.
        :param hotel: json - данные от сайта с отелями по локации.
        :return:
            response_data: dict: Словарь с данными по отелям.
        """
        response_data = dict()


        data_hotel = hotel["data"]["propertySearch"]["properties"]
        for id, hotel_info in enumerate(data_hotel):
            price = hotel_info["price"]["lead"]["amount"]
            # TODO : Требуется реализовать функцию подсчета дней которое пользователь будет жить в отеле.
            day = 1 # Временная переменная
            hotel = {"id": hotel_info["id"],
                     "name": hotel_info["name"],
                     "price_night": f"{round(price, 2)}$",
                     "price_total": f"{round(price * user_rental_day, 2)}$",
                     "rental_count": user_rental_day,
                     "reviews": {"score": hotel_info["reviews"]["score"], "total": hotel_info["reviews"]["total"]},
                     "description": "Hot springs Tokyo hotel with restaurant, connected to a shopping centre ",
                     "photo_image": hotel_info["propertyImage"]["image"]["url"],
                     }
            response_data.update({id + 1: hotel})

        return response_data

    def read_response_hotel(self, hotel: dict) -> dict:
        """
        Обрабатывает запрос от сайта по отелю.
        :param hotel: json - данные от сайта с отелями по локации.
        :return:
            response_data: список изображений
        """

        response_data = dict()
        image_response = list()
        data_hotel = hotel["data"]["propertyInfo"]["propertyGallery"]["images"]
        name = hotel["data"]["propertyInfo"]["summary"]["name"]

        for hotel_info in data_hotel:
            image_response.append(hotel_info["image"]["url"])

        response_data.update({"name": name,
                              "image": image_response
                              })
        return response_data

