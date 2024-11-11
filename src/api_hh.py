from typing import Any, Optional

import requests

from src.external_api import GetEmployersAPI, GetVacanciesAPI


class SearchVacanciesHH(GetVacanciesAPI):
    """Класс для Get-запросов на HeadHunter.ru"""

    def __init__(self, keywords: Optional = None, employer_id: Optional = None) -> None:
        """
        Метод инициализации объекта для Get-запросов на HeadHunter.ru,
        принимает ключевые слова для посика вакансий
        """
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        if keywords is not None and type(keywords) is str:
            keywords = keywords
        else:
            keywords = ""
        self.__params: dict[str, str | int] = {"page": 0, "per_page": 100, "text": keywords}
        if employer_id is not None:
            if type(employer_id) is str:
                self.__params["employer_id"] = employer_id
            else:
                raise TypeError("ID работодателя должно быть типа str")
        self.__status_code = None
        self.__vacancies: list[Any] = []

    def _request(self) -> None:
        """Метод Get-запроса на HeadHunter.ru"""
        self.__status_code = None
        try:
            response = requests.get(url=self.__url, headers=self.__headers, params=self.__params)
        except TypeError as error:
            print(f"{error} in {__file__}")
        else:
            self.__status_code = response.status_code
            if self.__status_code == 200:
                new_vacancies = response.json().get("items")
                self.__vacancies.extend(new_vacancies)
            else:
                raise AssertionError(f"Неуспешный статус-код: {self.__status_code}")

    def get_vacancies(self) -> list[dict[str, Any]]:
        """Метод получения вакансий с HeadHunter.ru"""
        while self.__params.get("page") < 20:
            self._request()
            self.__params["page"] += 1
        return self.__vacancies


class SearchEmployersHH(GetEmployersAPI):
    """Класс запроса к API hh.ru для получения информации по работодателям"""

    def __init__(self, keywords: Optional = None, active_vacancies: Optional = True) -> None:
        """Метод инизиализации атрибутов класса"""
        self.__url = "https://api.hh.ru/employers"
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        if keywords is not None and type(keywords) is str:
            keywords = keywords
        else:
            keywords = ""
        self.__params = {"page": 0, "per_page": 100, "text": keywords, "only_with_vacancies": active_vacancies}
        self.__status_code = None
        self.__employers: list[Any] = []

    def _request(self) -> None:
        """Метод запроса к API hh.ru"""
        self.__status_code = None
        try:
            response = requests.get(url=self.__url, headers=self.__headers, params=self.__params)
        except TypeError as error:
            print(f"{error} in {__file__}")
        else:
            self.__status_code = response.status_code
            if self.__status_code == 200:
                new_employers = response.json().get("items")
                self.__employers.extend(new_employers)

    def get_employers(self) -> list[dict[str, Any]]:
        """Метод получения информации о работодателях"""
        while self.__params.get("page") < 20:
            self._request()
            self.__params["page"] += 1
        return self.__employers
