import psycopg2
from config import get_params_db
from typing import Optional, Any
import re


class DBCreator:
    """Класс создания и удаления базы данных, создания и заполнения таблиц"""

    def __init__(self, db_name: str) -> None:
        """Метод инициализации объектов класса"""
        self.db_name = db_name
        self.__params = get_params_db()

    def create_db(self) -> None:
        """Метод создания базы данных"""
        conn = psycopg2.connect(**self.__params)
        try:
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {self.db_name}")
        finally:
            conn.close()
        print(f"База данных {self.db_name} успешно создана")

    def delete_db(self) -> None:
        """Метод удаления базы данных"""
        conn = psycopg2.connect(**self.__params)
        try:
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
                        f"FROM pg_stat_activity "
                        f"WHERE pg_stat_activity.datname = '{self.db_name}' "
                        f"AND pid <> pg_backend_pid()")
            cur.execute(f"DROP DATABASE {self.db_name}")
        except psycopg2.errors.InvalidCatalogName as err:
            print(f"Попытка удаления базы данных. {err}")
        finally:
            conn.close()

    def create_table(self, table_name: str, columns_dict: Optional = None) -> None:
        """Метод создания таблицы, принимает название таблицы и словарь с названиями колонок и типами данных,
        где ключ - название колонки, а значение - тип данных и ограничения колонки по канонам SQL"""
        self.__params["database"] = self.db_name
        conn = psycopg2.connect(**self.__params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(f"CREATE TABLE {table_name}(id serial PRIMARY KEY)")
                    if columns_dict is not None:
                        try:
                            for column_name, datatype in columns_dict.items():
                                cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {datatype}")
                        except TypeError:
                            pass
        finally:
            conn.close()
        self.__params.pop("database", None)
        print(f"Таблица {table_name} успешно создана")

    def insert_into_table_from_json(self, table_name: str, columns_str: str, json_data: list[dict[str, Any]]) -> None:
        """Метод добавления данных в таблицу, принимает название таблицы, строку с перечилением названий
        колонок, в которые будут добавляться данные, и данные для добавления в формате списка словарей"""
        self.__params["database"] = self.db_name
        conn = psycopg2.connect(**self.__params)
        try:
            with conn:
                with conn.cursor() as cur:
                    for dict_ in json_data:
                        list_values = []
                        for value in dict_.values():
                            list_values.append(value)
                        cur.execute(f"INSERT INTO {table_name} ({columns_str}) "
                                    f"VALUES ({re.sub(" ", ", ", "%s " * len(columns_str.split()),
                                                      count=(len(columns_str.split()) - 1))})",
                                    list_values)
        finally:
            conn.close()
        self.__params.pop("database", None)

    def add_foreign_key(self, table_name: str, column_name: str, other_table: str, other_column: str) -> None:
        """Метод добавления внешнего ключа таблицы, принимает названия таблиц и колонок для связывания"""
        self.__params["database"] = self.db_name
        conn = psycopg2.connect(**self.__params)
        try:
            with conn:
                with conn.cursor() as cur:
                    cur.execute(f"ALTER TABLE {table_name} "
                                f"ADD CONSTRAINT fk_{table_name}_{column_name} "
                                f"FOREIGN KEY({column_name}) "
                                f"REFERENCES {other_table}({other_column})")
        finally:
            conn.close()
        self.__params.pop("database", None)


class DBManager:
    """Класс получения данных из базы данных"""

    def __init__(self, db_name: str) -> None:
        """Метод инициализации объектов класса"""
        self.db_name = db_name
        self.__params = get_params_db()
        self.__params["database"] = db_name
        self.conn = psycopg2.connect(**self.__params)

    def get_select(self, select: str) -> list[tuple[Any, ...]]:
        """Метод для свободного запроса к базе данных"""
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute(select)
                    data = cur.fetchall()
        finally:
            pass
        return data

    def get_companies_and_vacancies_count(self) -> list[tuple[Any, ...]]:
        """Метод получения списка всех компаний и количество вакансий у каждой компании"""
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT employers.name, COUNT(*) "
                                "FROM vacancies "
                                "RIGHT JOIN employers "
                                "ON vacancies.employer_id = employers.id "
                                "GROUP BY employers.name")
                    data = cur.fetchall()
        finally:
            pass
        return data

    def get_all_vacancies(self) -> list[tuple[Any, ...]]:
        """Метод получения списка всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT employers.name, vacancies.name, salary_from, salary_to, "
                                "currency, vacancies.url "
                                "FROM vacancies "
                                "INNER JOIN employers "
                                "ON vacancies.employer_id = employers.id")
                    data = cur.fetchall()
        finally:
            pass
        return data

    def get_avg_salary(self) -> list[tuple[Any, ...]]:
        """Метод получения средней зарплаты по вакансиям"""
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT avg(sal_avg) "
                                "FROM (SELECT (salary_from + salary_to) / 2 as sal_avg "
                                "      FROM vacancies "
                                "      WHERE salary_from <> 0 or salary_to <> 0)")
                    data = cur.fetchall()
        finally:
            pass
        return data

    def get_vacancies_with_higher_salary(self) -> list[tuple[Any, ...]]:
        """Метод получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT vacancies.*, (salary_from + salary_to) / 2 as sal_avg "
                                "FROM vacancies "
                                "WHERE ((salary_from + salary_to) / 2) > "
                                "	   (SELECT avg(sal_avg)"
                                "		FROM (SELECT (salary_from + salary_to) / 2 as sal_avg "
                                "			  FROM vacancies "
                                "			  WHERE salary_from <> 0 or salary_to <> 0))")
                    data = cur.fetchall()
        finally:
            pass
        return data

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple[Any, ...]]:
        """Метод получения списка всех вакансий, в названии которых
        содержатся переданные в метод слова, например python"""
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute("select * "
                                "from vacancies "
                                f"where name ilike '%python%' or responsibility ilike '%{keyword}%'")
                    data = cur.fetchall()
        finally:
            pass
        return data

    def close_conn(self) -> None:
        self.conn.close()
