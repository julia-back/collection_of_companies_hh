from src.external_api import GetVacanciesAPI, GetEmployersAPI
from typing import Iterable, Any, Optional
import requests


class SearchVacanciesHH(GetVacanciesAPI):
    """Класс для Get-запросов на HeadHunter.ru"""

    def __init__(self, keywords=None, employer_id=None) -> None:
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
            self.__params["employer_id"] = employer_id
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

    def get_vacancies(self) -> Iterable:
        """Метод получения вакансий с HeadHunter.ru"""
        while self.__params.get("page") < 20:
            self._request()
            self.__params["page"] += 1
        return self.__vacancies


class SearchEmployersHH(GetEmployersAPI):

    def __init__(self, keywords=None, active_vacancies=True):
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

    def get_employers(self) -> Iterable:
        while self.__params.get("page") < 20:
            self._request()
            self.__params["page"] += 1
        return self.__employers
