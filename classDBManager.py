import psycopg2


class DBManager:

    def __init__(self, database_name, params):
        self.database_name = database_name
        self.params = params

    def get_companies_and_vacancies_count(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT company_name, COUNT(*) AS vacancies_amount
                FROM vacancies
                JOIN companies USING(company_id)
                GROUP BY company_name
                """
            )
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_all_vacancies(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT company_name, vacancy_name, salary, url
                FROM vacancies
                JOIN companies USING(company_id)
                """
            )
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_avg_salary(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary)
                FROM vacancies
                """
            )
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT vacancy_name
                FROM vacancies
                WHERE salary > (SELECT AVG(salary) FROM vacancies)
                """
            )
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword):
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT vacancy_name
                FROM vacancies
                WHERE vacancy_name LIKE '%{keyword}%'
                """
            )
            result = cur.fetchall()

        conn.commit()
        conn.close()
        return result
