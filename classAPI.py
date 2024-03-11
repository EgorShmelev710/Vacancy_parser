import requests


class API:

    def __init__(self, url):
        self.url = url

    def get_vacancies(self):
        params = {
            'employer_id': ([2180, 87021, 5331842, 816144, 27879, 1942330, 1025275, 49357, 9498112, 3529]),
            'per_page': 100,
            'only_with_salary': True
        }

        response = requests.get(self.url, params=params)
        vacancies = response.json()['items']
        return vacancies
