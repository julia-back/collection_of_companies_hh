import psycopg2
from config import get_params_db
from typing import Optional, Any
import re


class DBManager:

    def __init__(self, db_name):
        self.db_name = db_name
        self.__params = get_params_db()
        self.list_of_tables = []

    def create_db(self):
        conn = psycopg2.connect(**self.__params)
        try:
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE {self.db_name}")
        finally:
            conn.close()
        self.__params["database"] = self.db_name
        print(f"База данных {self.db_name} успешно создана")

    def delete_db(self):
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
        self.__params.pop("database", None)

    def create_table(self, table_name: str, columns_dict=None):
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
        self.list_of_tables.append(table_name)
        print(f"Таблица {table_name} успешно создана")

    def insert_into_table_from_json(self, table_name, columns_str: str, json_data: list[dict[str, Any]]):
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

    def add_foreign_key(self):
        pass

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        pass

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
         названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        pass
