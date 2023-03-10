from input_connect import InputConnect
from report import Report
from table import Table
from errors import OutOfDataError, SortParameterError, SortWayError, InstructionError


try:
    input_connect = InputConnect()
    if input_connect.is_statistic:
        report = Report()

        report.generate_excel(
            input_connect.all_salary_level,
            input_connect.all_vacancies_count,
            input_connect.salary_level,
            input_connect.vacancies_count,
            input_connect.by_city_level,
            input_connect.vacancies_part
        )
        report.generate_image(
            input_connect.filter_parameter,
            input_connect.all_salary_level,
            input_connect.all_vacancies_count,
            input_connect.salary_level,
            input_connect.vacancies_count,
            input_connect.by_city_level,
            input_connect.vacancies_part
        )
        report.generate_pdf(input_connect.filter_parameter)
        input_connect.print_self()
    else:
        print(Table(
            input_connect.vacancies,
            input_connect.filter,
            input_connect.sorter,
            input_connect.reversed,
            input_connect.output_range,
            input_connect.output_columns
        ))
except StopIteration:
    print("Пустой файл")
except IOError:
    print("Формат ввода некорректен")
except SortParameterError:
    print("Параметр сортировки некорректен")
except SortWayError:
    print("Порядок сортировки задан некорректно")
except KeyError:
    print("Параметр поиска некорректен")
except AssertionError:
    print("Ничего не найдено")
except InstructionError:
    print("Неверная комманда")
except OutOfDataError:
    print("Нет данных")
#ggggggggggggggg
