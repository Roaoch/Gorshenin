from data_set import DataSet
from utils import Utils
from errors import InstructionError, SortWayError
from typing import Dict
from datetime import datetime


class InputConnect:
    def __init__(self):
        self.__instruction = input("Введите комманду: ").strip().lower()
        self.__vacancies = DataSet(file_name=input("Введите название файла: ").strip())
        if self.is_statistic:
            self.filter_parameter = input("Введите название профессии: ").strip()
            self.all_salary_level = {}
            self.all_vacancies_count = {}
            self.salary_level = {}
            self.vacancies_count = {}
            self.by_city_level = {}
            self.vacancies_part = {}
            self.__get_statistics()
        elif self.is_vacancy:
            self.filter = self.get_filter(input("Введите параметр фильтрации: ").strip())
            self.sorter = input("Введите параметр сортировки: ").strip()
            self.reversed = self.get_sort_way(input("Обратный порядок сортировки (Да / Нет): ").strip())
            self.output_range = input("Введите диапазон вывода: ").strip().split(" ")
            self.output_columns = input("Введите требуемые столбцы: ").strip().split(", ")
        else:
            raise InstructionError

    @property
    def is_statistic(self) -> bool:
        return self.__instruction == "статистика"

    @property
    def is_vacancy(self) -> bool:
        return self.__instruction == "вакансии"

    @property
    def vacancies(self) -> str:
        return self.__vacancies.file_name

    def __get_statistics(self) -> None:
        temp_by_city_count = {}
        temp_by_city_level = {}
        temp_all_by_city_count = {}
        for vacancy in self.__vacancies.vacancies_reader:
            vacancy_year = vacancy.published_at.year
            vacancy_salary = vacancy.salary.get_salary()
            Utils.add_to_or_update(
                self.all_salary_level,
                vacancy_year,
                vacancy_salary
            )
            Utils.add_to_or_update(
                self.all_vacancies_count,
                vacancy_year,
                1
            )
            Utils.add_to_or_update(
                temp_by_city_level,
                vacancy.area_name,
                vacancy_salary
            )
            Utils.add_to_or_update(
                temp_all_by_city_count,
                vacancy.area_name,
                1
            )
            if self.filter_parameter in vacancy.name:
                Utils.add_to_or_update(
                    self.salary_level,
                    vacancy_year,
                    vacancy_salary
                )
                Utils.add_to_or_update(
                    self.vacancies_count,
                    vacancy_year,
                    1
                )
                Utils.add_to_or_update(
                    temp_by_city_count,
                    vacancy.area_name,
                    1
                )
        self.all_salary_level = {
            key: int(value / self.all_vacancies_count[key]) for key, value in self.all_salary_level.items()
        }
        self.salary_level = {
            key: int(value / self.vacancies_count[key]) for key, value in self.salary_level.items()
        }

        if len(self.salary_level) == 0:
            self.salary_level = {key: 0 for key in self.all_vacancies_count.keys()}
            self.vacancies_count = {key: 0 for key in self.all_vacancies_count.keys()}

        self.vacancies_part = self.__get_vacancy_part(temp_all_by_city_count)
        self.by_city_level = dict(sorted(
            [(key, int(temp_by_city_level[key] / temp_all_by_city_count[key])) for key in self.vacancies_part.keys()],
            key=lambda e: (e[1], -len(e[0])),
            reverse=True
        ))

    def print_self(self) -> None:
        print(f"Динамика уровня зарплат по годам: {self.all_salary_level}")
        print(f"Динамика количества вакансий по годам: {self.all_vacancies_count}")
        print(f"Динамика уровня зарплат по годам для выбранной профессии: {self.salary_level}")
        print(f"Динамика количества вакансий по годам для выбранной профессии: {self.vacancies_count}")
        print(f"Уровень зарплат по городам (в порядке убывания): {Utils.slice_dict(self.by_city_level, 10)}")
        print(f"Доля вакансий по городам (в порядке убывания): {Utils.slice_dict(self.vacancies_part, 10)}")

    @staticmethod
    def get_filter(string: str) -> tuple or None:
        filter_name_to_parse = {
            "key_skills": lambda to_parse:
            to_parse.split(", "),
            "salary": lambda to_parse:
            int(to_parse),
            "published_at": lambda to_parse:
            datetime.strptime(to_parse, "%d.%m.%Y"),
            "experience_id": lambda to_parse:
            Utils.inverse_dict(Utils.translation_experience)[to_parse],
            "premium": lambda to_parse:
            Utils.inverse_dict(Utils.translation_premium)[to_parse],
            "salary_currency": lambda to_parse:
            Utils.inverse_dict(Utils.translation_currency)[to_parse]
        }

        if string == '':
            return None
        if not string.__contains__(':'):
            raise IOError

        filter_rules = [x.strip() for x in string.split(':')]
        if not Utils.translation_filter.__contains__(filter_rules[0]):
            raise KeyError
        filter_name = Utils.translation_filter[filter_rules[0]]
        if filter_name_to_parse.__contains__(filter_name):
            filter_object = filter_name_to_parse[filter_name](filter_rules[1])
        else:
            filter_object = filter_rules[1]

        return filter_name, filter_object

    @staticmethod
    def get_sort_way(to_parse: str) -> bool:
        if to_parse == "Да":
            return True
        elif to_parse == "Нет" or to_parse == "":
            return False
        else:
            raise SortWayError

    @staticmethod
    def __get_vacancy_part(by_city_count: Dict[str, int]):
        result = []
        all_vacancy_count = sum(by_city_count.values())
        for key, value in by_city_count.items():
            part = value / all_vacancy_count
            if part >= 0.01:
                result.append((key, float("{:.4f}".format(part))))
        return dict(sorted(
            result,
            key=lambda e: e[1],
            reverse=True
        ))
