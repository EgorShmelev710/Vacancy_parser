from config import config
from utils import create_database, save_data_to_database
from classAPI import API
from classDBManager import DBManager


def main():
    params = config()

    api = API('https://api.hh.ru/vacancies')
    hh_vacancies = api.get_vacancies()
    dbmanager = DBManager('work', params)

    create_database('work', params=params)
    save_data_to_database(hh_vacancies, 'work', params)
    print(dbmanager.get_companies_and_vacancies_count())
    print(dbmanager.get_all_vacancies())
    print(dbmanager.get_avg_salary())
    print(dbmanager.get_vacancies_with_higher_salary())
    print(dbmanager.get_vacancies_with_keyword('Специалист'))


if __name__ == '__main__':
    main()
