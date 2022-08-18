import psycopg2

from data.config import DB_URI

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()


def add_record(data: list) -> None:
    """
    Создает запить в базе данных
    """
    pass


def write_to_excel() -> None:
    """
    Переписывает реест из базы данных в excel файл
    """
    pass


def get_users_id() -> list:
    """
    Возвращает список id всех инициаторов платежей
    """
    pass


def get_files_id(user_id: int) -> list:
    """
    Возвращает список id всех файлов с сервера Telegram
    user_id - id инициатора
    """
    pass
