from unittest.mock import patch, MagicMock
from src.file_DBmanager import DBManager


@patch('src.get_DBManager.psycopg2.connect')
def test_get_companies_and_vacancies_count(mock_connect, db_manager):
    # Настройка имитации курсора и результата
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Company A', 5), ('Company B', 3)]

    result = db_manager.get_companies_and_vacancies_count()
    for i in result:
        print(i)
    print(result)
    assert result == [('Company A', 5), ('Company B', 3)]
    mock_cursor.execute.assert_called_once_with("""
                SELECT employer_name, COUNT(vacancies.employer_id)
                FROM employers
                INNER JOIN vacancies USING (employer_id)
                GROUP BY employer_name
                ORDER BY COUNT DESC
    """)


@patch('src.get_DBManager.psycopg2.connect')
def test_get_all_vacancies(mock_connect, db_manager):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('Company A', 'Vacancy A', 1000, 2000, 'http://example.com/vacancy_a'),
        ('Company B', 'Vacancy B', 1500, 2500, 'http://example.com/vacancy_b'),
    ]

    result = db_manager.get_all_vacancies()

    assert result == [
        ('Company A', 'Vacancy A', 1000, 2000, 'http://example.com/vacancy_a'),
        ('Company B', 'Vacancy B', 1500, 2500, 'http://example.com/vacancy_b'),
    ]
    mock_cursor.execute.assert_called_once_with("""
        SELECT employer_name,
        vacancy_name,
        salary_from,
        salary_to,
        url
        FROM vacancies
    """)


@patch('src.get_DBManager.psycopg2.connect')
def test_get_avg_salary(mock_connect, db_manager):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Company A', 1500), ('Company B', 2000)]

    result = db_manager.get_avg_salary()

    assert result == [('Company A', 1500), ('Company B', 2000)]
    mock_cursor.execute.assert_called_once_with("""
        SELECT employer_name,
        AVG((salary_from + salary_to) / 2) AS average_salary
        FROM vacancies
        WHERE salary_from IS NOT NULL
        AND salary_to IS NOT NULL
        GROUP BY employer_name
    """)


@patch('src.get_DBManager.psycopg2.connect')
def test_get_vacancies_with_higher_salary(mock_connect, db_manager):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Vacancy A',), ('Vacancy B',)]

    result = db_manager.get_vacancies_with_higher_salary()

    assert result == [('Vacancy A',), ('Vacancy B',)]
    mock_cursor.execute.assert_called_once_with("""
        SELECT * FROM vacancies
        WHERE (salary_from + salary_to) / 2 > (
        SELECT AVG((salary_from + salary_to) / 2)
        FROM vacancies)
    """)


@patch('src.get_DBManager.psycopg2.connect')
def test_get_vacancies_with_keyword(mock_connect, db_manager):
    keyword = 'developer'
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('Developer Vacancy',)]

    result = db_manager.get_vacancies_with_keyword(keyword)

    assert result == [('Developer Vacancy',)]
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM vacancies"
        " WHERE vacancy_name ILIKE %s", ('%developer%',)
    )

