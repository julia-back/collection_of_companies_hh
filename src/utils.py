from typing import Iterable, Any
from re import sub


def clear_hh_vacancies_by_keys(vacancies_list: Iterable[dict[Any, Any]]) -> list[dict[str, Any]]:
    """Функция преобразования вакансий с hh.ru словаря в словарь с нужными данными"""
    clear_vacancies = []
    for vacancy_dict in vacancies_list:
        id_ = vacancy_dict.get("id")
        name = vacancy_dict.get("name")
        area = vacancy_dict.get("area").get("name")
        if vacancy_dict.get("salary") is None:
            salary_from = 0
            salary_to = 0
            currency = "RUR"
        else:
            salary_from = vacancy_dict.get("salary").get("from")
            salary_to = vacancy_dict.get("salary").get("to")
            currency = vacancy_dict.get("salary").get("currency")
        alternate_url = vacancy_dict.get("alternate_url")
        responsibility = vacancy_dict.get("snippet").get("responsibility")
        responsibility = sub(r"<([a-z]|/)+>", "", responsibility) if responsibility is not None else responsibility
        experience = vacancy_dict.get("experience").get("name")
        dict_vacancy = {"id_hh": id_, "name": name, "area": area, "salary_from": salary_from,
                        "salary_to": salary_to, "currency": currency,
                        "url": alternate_url, "responsibility": responsibility,
                        "experience": experience}
        clear_vacancies.append(dict_vacancy)
    return clear_vacancies


def clear_hh_employers_by_keys(employers_list: Iterable[dict[Any, Any]]) -> list[dict[str, Any]]:
    clear_list_employers = []
    for employer in employers_list:
        id_ = employer.get("id")
        name = employer.get("name")
        url = employer.get("alternate_url")
        dict_employer = {"id_hh": id_, "name": name, "url": url}
        clear_list_employers.append(dict_employer)
    return clear_list_employers


def get_my_employers(employers: Iterable[dict[Any, Any]], id_list) -> list[dict[str, Any]]:
    my_employers = []
    for employer in employers:
        if employer.get("id_hh") in id_list:
            my_employers.append(employer)
    return my_employers
