from pprint import pprint
import requests


class HH:
    """Класс для работы с API HH"""

    def __init__(
        self,
    ):
        """конструктор класса"""
        self.__url = "https://api.hh.ru/"
        self._headers = {"User-Agent": "HH-User-Agent"}
        self._params = {"per_page": 100, "page": 0, "only_with_salary": True}
        self.employers = [
            6062708,
            78638,
            10571093,
            198614,
            5667343,
            901808,
            774144,
            9694561,
            4219,
            5919632,
        ]

    def get_employers(self):
        """загрузка списка работодателей"""
        employers_info = []
        for employer_id in self.employers:
            temp_url = f"{self.__url}employers/{employer_id}"
            try:
                employer_data = requests.get(temp_url)
                employer_data.raise_for_status()
                employers_info.append(employer_data.json())
            except requests.exceptions.RequestException as e:
                print(f"Error fetching employer {employer_id}: {e}")

        return employers_info

    def load_vacancies(self):
        """загрузка вакансий"""
        vacancy_info = []
        for employer_id in self.employers:
            self._params["employer_id"] = employer_id
            vacancy_url = f"{self.__url}vacancies"
            response = requests.get(
                vacancy_url, headers=self._headers, params=self._params
            )
            vacancies = response.json()["items"]
            vacancy_info.extend(vacancies)

        return vacancy_info


if __name__ == "__main__":
    data_employer = HH().get_employers()
    data_vacancies = HH().load_vacancies()

    pprint(data_employer)
    pprint(data_vacancies)
