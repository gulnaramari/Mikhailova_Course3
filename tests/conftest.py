import pytest

from src.file_DBmanager import DBManager


@pytest.fixture
def manager():
    """Фикстура для создания экземпляра DBManager."""
    params = {'user': 'postgres', 'password': 'Mariam', 'host': 'localhost'}
    return DBManager(params)
