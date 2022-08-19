import psycopg2
import logging

from data.config import DB_URI


def add_record(data: list) -> None:
    """
    Создает запить в базе данных
    """
    try:
        db_connection = psycopg2.connect(DB_URI, sslmode="require")
        db_object = db_connection.cursor()

        db_object.execute(
            "INSERT INTO register(id, date_of_application, payment_iniciator, basis_of_payment, payment_sum, payment_amount, payment_recipient, purpose_of_payment, payment_deadline) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
        db_connection.commit()
    except Exception as err:
        logging.exception(err)


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
