from src.api_hh import SearchVacanciesHH, SearchEmployersHH
from src.utils import clear_hh_vacancies_by_keys, clear_hh_employers_by_keys, get_my_employers
from src.database_manager import DBManager, DBCreator


columns_vacancies = {"id_hh": "varchar(10)", "name": "varchar(100)", "area": "varchar(255)",
                     "salary_from": "int", "salary_to": "int", "currency": "varchar(5)",
                     "url": "varchar(255)", "responsibility": "text", "experience": "varchar(100)",
                     "employer_id": "int"}
columns_employers = {"id_hh": "varchar(10)", "name": "varchar(100)", "url": "varchar(255)"}


def creator():
    db = DBCreator("hh_db")
    db.delete_db()
    db.create_db()
    db.create_table("vacancies", columns_dict=columns_vacancies)
    db.create_table("employers", columns_dict=columns_employers)
    print("Добавляем данные в таблицы...")

    employers = SearchEmployersHH(keywords="IT").get_employers()
    employers = clear_hh_employers_by_keys(employers)
    employers = get_my_employers(employers, ["9802693", "3529", "78638", "26250",
                                             "1049556", "3776", "534346", "11586206",
                                             "4019151", "960261"])
    db.insert_into_table_from_json("employers", "id_hh, name, url", employers)

    db_get = DBManager("hh_db")
    for employer in employers:
        id_hh = employer.get("id_hh")
        id_ = (db_get.get_select(f"SELECT id FROM employers WHERE id_hh = '{id_hh}'"))[0][0]
        vacancies_by_employer = SearchVacanciesHH(employer_id=id_hh).get_vacancies()
        vacancies_by_employer = clear_hh_vacancies_by_keys(vacancies_by_employer)
        for vacancy in vacancies_by_employer:
            vacancy["employer_id"] = id_
        db.insert_into_table_from_json("vacancies",
                                       "id_hh, name, area, salary_from, "
                                       "salary_to, currency, url, responsibility, "
                                       "experience, employer_id", vacancies_by_employer)

    db.add_foreign_key("vacancies", "employer_id", "employers", "id")
    print("Создание базы данных и добавление в нее данных прошло успешно")


def main():
    user_input = input("Создать базу данных? да/нет\n")
    if user_input.lower() == "да":
        creator()
    db = DBManager("hh_db")
    try:
        user_input = 0
        while user_input != "6":
            user_input = input("\nВыверите метод получения данных или выход из программы:\n"
                               "1 - получить количество вакансий у каждой компании\n"
                               "2 - получить список всех вакансий\n"
                               "3 - получить среднюю зарплату по вакансиям\n"
                               "4 - получить список вакансий, у которых зарплата выше средней\n"
                               "5 - получить вакансии по ключевому слову\n"
                               "6 - выход\n")
            if user_input == "1":
                companies_and_vacancies_count = db.get_companies_and_vacancies_count()
                for company in companies_and_vacancies_count:
                    print(f"'{company[0]}', кол-во сотрудников: {company[1]}.")
            elif user_input == "2":
                all_vacancies = db.get_all_vacancies()
                print(all_vacancies)
                for vacancy in all_vacancies:
                    if vacancy[2] not in [None, 0] and vacancy[3] not in [None, 0]:
                        print(f"{vacancy[0]}, {vacancy[1]}, "
                              f"\nЗарплата: {vacancy[2]} - {vacancy[3]} {vacancy[4]}, "
                              f"\nСсылка: {vacancy[5]}\n")
                    elif vacancy[2] not in [None, 0] and vacancy[3] in [None, 0]:
                        print(f"{vacancy[0]}, {vacancy[1]}, "
                              f"\nЗарплата: от {vacancy[2]} {vacancy[4]}, "
                              f"\nСсылка: {vacancy[5]}\n")
                    elif vacancy[3] not in [None, 0] and vacancy[2] in [None, 0]:
                        print(f"{vacancy[0]}, {vacancy[1]}, "
                              f"\nЗарплата: до {vacancy[3]} {vacancy[4]}, "
                              f"\nСсылка: {vacancy[5]}\n")
                    else:
                        print(f"{vacancy[0]}, {vacancy[1]}, "
                              f"\nЗарплата: не указана, "
                              f"\nСсылка: {vacancy[5]}\n")
            elif user_input == "3":
                print(f"Средняя зарплата по всем вакансиям: {round(db.get_avg_salary()[0][0])}")
            elif user_input == "4":
                vacancies_with_higher_salary = db.get_vacancies_with_higher_salary()
                print(vacancies_with_higher_salary)
                for vacancy in vacancies_with_higher_salary:
                    if vacancy[4] not in [None, 0] and vacancy[5] not in [None, 0]:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: {vacancy[4]} - {vacancy[5]} {vacancy[6]}, "
                              f"\nСсылка: {vacancy[7]}\n")
                    elif vacancy[4] not in [None, 0] and vacancy[5] in [None, 0]:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: от {vacancy[4]} {vacancy[6]}, "
                              f"\nСсылка: {vacancy[7]}\n")
                    elif vacancy[5] not in [None, 0] and vacancy[4] in [None, 0]:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: до {vacancy[5]} {vacancy[6]}, "
                              f"\nСсылка: {vacancy[7]}\n")
                    else:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: не указана, "
                              f"\nСсылка: {vacancy[7]}\n")
            elif user_input == "5":
                vacancies_with_keyword = db.get_vacancies_with_keyword("python")
                for vacancy in vacancies_with_keyword:
                    if vacancy[4] not in [None, 0] and vacancy[5] not in [None, 0]:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: {vacancy[4]} - {vacancy[5]} {vacancy[6]}, "
                              f"\nСсылка: {vacancy[7]}\n")
                    elif vacancy[4] not in [None, 0] and vacancy[5] in [None, 0]:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: от {vacancy[4]} {vacancy[6]}, "
                              f"\nСсылка: {vacancy[7]}\n")
                    elif vacancy[5] not in [None, 0] and vacancy[4] in [None, 0]:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: до {vacancy[5]} {vacancy[6]}, "
                              f"\nСсылка: {vacancy[7]}\n")
                    else:
                        print(f"{vacancy[2]}, "
                              f"\nЗарплата: не указана, "
                              f"\nСсылка: {vacancy[7]}\n")
    finally:
        db.close_conn()


if __name__ == "__main__":
    main()
