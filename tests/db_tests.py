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
