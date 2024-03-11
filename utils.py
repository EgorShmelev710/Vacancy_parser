import psycopg2


def create_database(database_name, params):
    conn = psycopg2.connect(dbname='postgres', **params)
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE companies (
            company_id int PRIMARY KEY,
            company_name varchar(100) NOT NULL
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
            vacancy_id int PRIMARY KEY,
            company_id int REFERENCES companies(company_id) NOT NULL,
            vacancy_name varchar(100) NOT NULL,
            salary int,
            currency varchar,
            url varchar
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data, database_name, params):
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        distinct_companies = []
        for vacancy in data:
            if vacancy['employer']['id'] not in distinct_companies:
                distinct_companies.append(vacancy['employer']['id'])
                cur.execute(
                    """
                    INSERT INTO companies (company_id, company_name)
                    VALUES (%s, %s)
                    """,
                    (vacancy['employer']['id'], vacancy['employer']['name'])
                )
            vacancy_salary = vacancy['salary']['to'] if vacancy['salary']['to'] else vacancy['salary']['from']
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, company_id, vacancy_name, salary, currency, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id'], vacancy['employer']['id'], vacancy['name'], vacancy_salary,
                 vacancy['salary']['currency'], vacancy['alternate_url'])
            )

    conn.commit()
    conn.close()
