from errors import SortParameterError
from vacancy import Vacancy
from data_set import DataSet
from utils import Utils
from datetime import datetime
from prettytable import PrettyTable
from typing import List, Generator, Callable


class Table:
    __sorter = {
        "Навыки": lambda to_sort:
        len(to_sort.key_skills),
        "Оклад": lambda to_sort:
        (float(to_sort.salary.salary_from) + float(to_sort.salary.salary_to))
        / 2 * Utils.currency_to_rub[to_sort.salary.salary_currency],
        "Опыт работы": lambda to_sort:
        Utils.experience_to_int[to_sort.experience_id],
        "Название": lambda to_sort:
        to_sort.name,
        "Описание": lambda to_sort:
        to_sort.description,
        "Премиум-вакансия": lambda to_sort:
        to_sort.premium,
        "Компания": lambda to_sort:
        to_sort.employer_name,
        "Название региона": lambda to_sort:
        to_sort.area_name,
        "Дата публикации вакансии": lambda to_sort:
        to_sort.published_at
    }
    __formatter = {
        lambda row: row.__setattr__("description", row.description.strip()),
        lambda row: row.__setattr__("key_skills", "\n".join(row.key_skills)),
        lambda row: row.__setattr__("premium", Utils.translation_premium[row.premium.capitalize()]),
        lambda row: row.__setattr__("experience_id", Utils.translation_experience[row.experience_id]),
        lambda row: row.__setattr__("published_at", datetime.strftime(row.published_at, "%d.%m.%Y"))
    }

    def __init__(
            self,
            filename,
            filter_parameter,
            sort_parameter,
            is_revers,
            print_range,
            print_columns

    ):
        self.vacancies = DataSet(file_name=filename)
        self.filter_parameter = filter_parameter
        self.sort_parameter = sort_parameter
        self.is_revers = is_revers
        self.print_range = print_range
        self.print_columns = print_columns
        self.filter_vacancies()

    def __str__(self):
        my_table = PrettyTable()
        row_count = 0
        my_table.field_names = [
            "№",
            "Название",
            "Описание",
            "Навыки",
            "Опыт работы",
            "Премиум-вакансия",
            "Компания",
            "Оклад",
            "Название региона",
            "Дата публикации вакансии"
        ]
        for row in self.get_sorted(self.sort_parameter, self.is_revers):
            row_count += 1
            my_table.add_row([row_count.__str__()] + self.make_table_row(row))

        if row_count == 0:
            raise AssertionError

        self.format_table(my_table)

        if self.print_columns[0] == '':
            self.print_columns = my_table.field_names
        else:
            self.print_columns.insert(0, "№")
        if self.print_range[0] == '':
            self.print_range = [1, row_count + 1]
        elif len(self.print_range) < 2:
            self.print_range.append(str(row_count + 1))

        return my_table.get_string(
            fields=self.print_columns,
            start=int(self.print_range[0]) - 1,
            end=int(self.print_range[1]) - 1
        )

    def make_table_row(self, vacancy) -> List[any]:
        result = []
        for formatting in self.__formatter:
            formatting(vacancy)

        for attribute in vacancy.__dict__:
            attribute_value = vacancy.__getattribute__(attribute)
            if len(attribute_value.__str__()) > 100:
                attribute_value = attribute_value.__str__()[:100] + "..."
            result.append(attribute_value)
        return result

    def get_sorted(self, sort_parameter: Callable, is_revers: bool) -> List[Vacancy] or Generator[Vacancy, None, None]:
        if sort_parameter == "":
            return self.vacancies.vacancies_reader
        elif self.__sorter.__contains__(sort_parameter):
            sort_key = self.__sorter[sort_parameter]
        else:
            raise SortParameterError
        return sorted(list(self.vacancies.vacancies_reader), key=sort_key, reverse=is_revers)

    @staticmethod
    def format_table(table: PrettyTable) -> None:
        table.hrules = 1
        table.max_width = 20
        table.min_width = 20
        table._min_width = {"№": 0}
        table.align = 'l'

    def filter_vacancies(self):
        filter_checker = {
            "key_skills": lambda vacancy:
            all(x in vacancy.key_skills for x in self.filter_parameter[1]),
            "salary": lambda vacancy:
            int(vacancy.salary.salary_from) <= self.filter_parameter[1] <= int(vacancy.salary.salary_to),
            "published_at": lambda vacancy:
            all([
                vacancy.published_at.year == self.filter_parameter[1].year,
                vacancy.published_at.month == self.filter_parameter[1].month,
                vacancy.published_at.day == self.filter_parameter[1].day
            ]),
            "experience_id": lambda vacancy:
            vacancy.experience_id == self.filter_parameter[1],
            "premium": lambda vacancy:
            vacancy.premium == self.filter_parameter[1],
            "salary_currency": lambda vacancy:
            vacancy.salary.salary_currency == self.filter_parameter[1],
            "name": lambda vacancy:
            vacancy.name == self.filter_parameter[1],
            "area_name": lambda vacancy:
            vacancy.area_name == self.filter_parameter[1],
            "employer_name": lambda vacancy:
            vacancy.employer_name == self.filter_parameter[1],
            "description": lambda vacancy:
            vacancy.description == self.filter_parameter[1]
        }

        if self.filter_parameter:
            self.vacancies.vacancies_reader = filter(
                filter_checker[self.filter_parameter[0]],
                self.vacancies.vacancies_reader
            )
