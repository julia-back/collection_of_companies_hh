from src.api_hh import SearchVacanciesHH, SearchEmployersHH
from src.utils import clear_hh_vacancies_by_keys, clear_hh_employers_by_keys, get_my_employers
from src.database_manager import DBManager
import re


columns_vacancies = {"id_hh": "varchar(10)", "name": "varchar(100)", "area": "varchar(255)",
                     "salary_from": "int", "salary_to": "int", "currency": "varchar(5)",
                     "url": "varchar(255)", "responsibility": "text", "experience": "varchar(100)",
                     "employer_id": "varchar(10)"}
columns_employers = {"id_hh": "int", "name": "varchar(100)", "url": "varchar(255)"}


def main():
    db = DBManager("hh_db")
    # db.delete_db()
    # db.create_db()
    # db.create_table("vacancies", columns_dict=columns_vacancies)
    # db.create_table("employers", columns_dict=columns_employers)
    # print("create tables")
    #
    # employers = SearchEmployersHH(keywords="IT").get_employers()
    # print("get employers")
    # employers = clear_hh_employers_by_keys(employers)
    # employers = get_my_employers(employers, ["9802693", "3529", "78638", "26250",
    #                                          "1049556", "3776", "534346", "11586206",
    #                                          "4019151", "960261"])
    # db.insert_into_table_from_json("employers", "id_hh, name, url", employers)
    # print("add employers in db")
    #
    # for employer in employers:
    #     employer_id = employer.get("id_hh")
    #     print(employer_id)
    #     vacancies_by_employer = SearchVacanciesHH(employer_id=employer_id).get_vacancies()
    #     print("get one vacancies list", employer_id)
    #     vacancies_by_employer = clear_hh_vacancies_by_keys(vacancies_by_employer)
    #     for vacancy in vacancies_by_employer:
    #         vacancy["employer_id"] = employer_id
    #     db.insert_into_table_from_json("vacancies",
    #                                    "id_hh, name, area, salary_from, "
    #                                    "salary_to, currency, url, responsibility, "
    #                                    "experience, employer_id", vacancies_by_employer)
    #     print("add vacancies in db")
    pass


if __name__ == "__main__":
    main()
