from decimal import Decimal
from typing import Any, List, Dict

import psycopg2


class DBManager:
    def __init__(self, params):
        """Класс, который будет подключаться к БД PostgreSQL
        и иметь методы: 1.get_companies_and_vacancies_count() — получает список всех компаний
        и количество вакансий у каждой компании.2.get_all_vacancies() — получает список всех вакансий
        с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        3.get_avg_salary() — получает среднюю зарплату по вакансиям.
        4.get_vacancies_with_higher_salary() получает список всех вакансий, у которых зарплата
        выше средней по всем вакансиям.5.get_vacancies_with_keyword()
        получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python."""
        # Получаем параметры подключения из файла
        self.host = params["host"]
        self.user = params["user"]
        self.password = params["password"]
        self.port = params["port"]

        # Подключаемся к только что созданной базе данных
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port,
            database="course3_hh",
        )
        self.cursor = self.connection.cursor()

    def close(self):
        """
        Закрывает текущее соединение с базой данных и курсор.

        Этот метод должен вызываться, когда работа с базой данных завершена, чтобы освободить ресурсы.
        """
        self.cursor.close()
        self.connection.close()

    def get_companies_and_vacancies_count(self) -> List:
        """
        Получает список компаний и количество вакансий для каждой компании.

        :return: Список кортежей, где каждый кортеж содержит имя компании и количество вакансий.
        """
        self.cursor.execute(
            """
                           SELECT employer_name, COUNT(vacancies.employer_id)
                           FROM employers
                           INNER JOIN vacancies USING (employer_id)
                           GROUP BY employer_name
                           ORDER BY COUNT DESC
                   """
        )

        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List:
        """
        Получает все вакансии с информацией о компании.

        :return: Список кортежей, где каждый кортеж содержит имя компании, название вакансии, зарплату и URL.
        """
        self.cursor.execute(
            """
                            SELECT e.employer_name, v.vacancy_name, v.salary, v.vacancy_url
                            FROM vacancies v
                            INNER JOIN employers e USING (employer_id)
                            WHERE v.salary IS NOT NULL AND v.salary != 0
                            ORDER BY v.salary DESC

                    """
        )

        return self.cursor.fetchall()

    def get_avg_salary(self) -> Any:
        """получает среднюю зарплату по вакансиям."""
        self.cursor.execute(
            """
                       SELECT AVG(salary)
                       FROM vacancies
               """
        )

        result = self.cursor.fetchone()
        avg_salary = Decimal(result[0])
        formatted_avg_salary = format(avg_salary, ".2f")
        return formatted_avg_salary

    def get_vacancies_with_higher_salary(self) -> List:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()[0][0]

        self.cursor.execute(
            """
            SELECT v.vacancy_name, v.salary
            FROM vacancies v
            WHERE v.salary > %s;
            """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword) -> List:
        """
        Получает вакансии, в названии которых содержится заданное ключевое слово.

        :param keyword: Ключевое слово для поиска в названиях вакансий.
        :return: Список кортежей, где каждый кортеж содержит имя компании, название вакансии, зарплату и URL.
        """
        keyword = f"%{keyword.lower()}%"
        self.cursor.execute(
            """
                            SELECT vacancy_name
                            FROM vacancies
                            WHERE vacancy_name LIKE %s
                    """,
            (keyword,),
        )

        return self.cursor.fetchall()
