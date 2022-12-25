from typing import List
from utils import Utils


class Salary:
    def __init__(self, salary_property: List[str]):
        self.salary_from = float(salary_property[0])
        self.salary_to = float(salary_property[1])
        if len(salary_property) == 4:
            self.salary_gross = salary_property[2]
            self.salary_currency = salary_property[3]
        else:
            self.salary_currency = salary_property[2]

    def __str__(self):
        return "{0} - {1} ({2}) ({3})".format(
            Utils.format_float(self.salary_from),
            Utils.format_float(self.salary_to),
            Utils.translation_currency[self.salary_currency],
            Utils.translation_gross[self.salary_gross]
        )

    def get_salary(self) -> float:
        return (self.salary_from + self.salary_to) / 2 * Utils.currency_to_rub[self.salary_currency]