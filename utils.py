from typing import Dict, List


class Utils:
    currency_to_rub = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    translation_currency = {
        "AZN": "Манаты",
        "BYR": "Белорусские рубли",
        "EUR": "Евро",
        "GEL": "Грузинский лари",
        "KGS": "Киргизский сом",
        "KZT": "Тенге",
        "RUR": "Рубли",
        "UAH": "Гривны",
        "USD": "Доллары",
        "UZS": "Узбекский сум",
    }
    translation_gross = {
        "False": "С вычетом налогов",
        "True": "Без вычета налогов"
    }
    translation_filter = {
        "Навыки": "key_skills",
        "Оклад": "salary",
        "Дата публикации вакансии": "published_at",
        "Опыт работы": "experience_id",
        "Премиум-вакансия": "premium",
        "Идентификатор валюты оклада": "salary_currency",
        "Название": "name",
        "Название региона": "area_name",
        "Компания": "employer_name",
        "Описание": "description"
    }
    translation_experience = {
        "noExperience": "Нет опыта",
        "between1And3": "От 1 года до 3 лет",
        "between3And6": "От 3 до 6 лет",
        "moreThan6": "Более 6 лет"
    }
    experience_to_int = {
        "noExperience": 1,
        "between1And3": 2,
        "between3And6": 3,
        "moreThan6": 4
    }
    translation_premium = {
        "False": "Нет",
        "True": "Да"
    }

    @staticmethod
    def format_float(salary: float) -> str:
        return "{:,.0f}".format(salary).replace(',', ' ')

    @staticmethod
    def inverse_dict(straight: dict) -> dict:
        return {v: k for k, v in straight.items()}

    @staticmethod
    def add_to_or_update(dictionary: Dict[any, any], key: any, value: any) -> None:
        if dictionary.__contains__(key):
            dictionary[key] += value
        else:
            dictionary.update({key: value})

    @staticmethod
    def slice_dict(dictionary: dict, end: int):
        result = {}
        i = 0
        for key, value in dictionary.items():
            i += 1
            if i <= end:
                result.update({key: value})
            else:
                break
        return result

    @staticmethod
    def dict_difference(sliced_dict: Dict[str, float], full_dict: Dict[str, float]) -> Dict[str, float]:
        return {key: full_dict[key] for key in full_dict.keys() if key not in sliced_dict.keys()}

    @staticmethod
    def wrap_text(text: str, separators: List[str]):
        result = text
        for sep in separators:
            if text.__contains__(sep):
                result = "\n".join(text.split(sep, 1))
                break
        return result
