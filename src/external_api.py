from abc import ABC, abstractmethod
from typing import Iterable


class RequestAPI(ABC):
    """Общий абстрактный класс API-запросов"""

    @abstractmethod
    def _request(self) -> None:
        """Абстрактный метод запроса"""
        pass


class GetRequestAPI(RequestAPI, ABC):
    """Абстрактный класс Get-запросов"""

    @abstractmethod
    def _request(self) -> None:
        """Абстрактный метод Get-запроса"""
        pass


class PostRequestAPI(RequestAPI, ABC):
    """Абстрактный класс Post-запросов"""

    @abstractmethod
    def _request(self) -> None:
        """Абстрактный метод Post-запроса"""
        pass


class GetVacanciesAPI(GetRequestAPI, ABC):
    """Абстрактный класс Get-запросов на API с вакансиями"""

    @abstractmethod
    def _request(self) -> None:
        """Абстрактный метод Get-запросов на API с вакансиями"""
        pass

    @abstractmethod
    def get_vacancies(self) -> Iterable:
        """Абстрактный метод получения вакансий (обращается к методу запроса __request)"""
        pass


class GetEmployersAPI(GetRequestAPI, ABC):
    """Абстрактный класс Get-запросов на API с информацией о работодателях"""

    @abstractmethod
    def _request(self) -> None:
        """Абстрактный метод Get-запросов на API с информацией о работодателях"""
        pass

    @abstractmethod
    def get_employers(self) -> Iterable:
        """Абстрактный метод получения информации о работодателях (обращается к методу запроса __request)"""
        pass
