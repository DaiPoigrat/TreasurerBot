import psycopg2
import logging
import openpyxl
from aiogram.types import InputFile
from yandex_disk import upload_register

from data.config import DB_URI

titles = ['Дата поступления', 'Инициатор платежа', 'Основание платежа', 'id документа', 'Сумма платежа',
          'Размер оплаты', 'Получатель', 'Назначение', 'Крайний срок оплаты', 'Тип']


def add_record(data: list) -> None:
    """
    Создает запить в базе данных
    """
    try:
        db_connection = psycopg2.connect(DB_URI, sslmode="require")
        db_object = db_connection.cursor()

        db_object.execute(
            "INSERT INTO register(id, date_of_application, payment_iniciator, basis_of_payment, file_id, payment_sum, payment_amount, payment_recipient, purpose_of_payment, payment_deadline, type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]))
        db_connection.commit()

        doc = openpyxl.open('data/register.xlsx')
        doc.worksheets[0].append(data[1:])
        doc.save('data/register.xlsx')
        upload_register()
    except Exception as err:
        logging.exception(err)


def write_to_excel() -> None:
    """
    Переписывает реест из базы данных в excel файл
    """
    try:
        db_connection = psycopg2.connect(DB_URI, sslmode="require")
        db_object = db_connection.cursor()

        db_object.execute(
            "SELECT date_of_application, payment_iniciator, basis_of_payment, file_id, payment_sum, payment_amount, payment_recipient, purpose_of_payment, payment_deadline, type FROM register"
        )

        result = db_object.fetchall()

        doc = openpyxl.open(filename='data/database.xlsx')
        doc.create_sheet(title='Заявки', index=0)
        sheet = doc.worksheets[0]
        sheet.append(titles)

        for row in result:
            sheet.append([str(item).rstrip() for item in row])

        doc.save(filename='data/database.xlsx')
    except Exception as err:
        logging.exception(err)


def drop_excel() -> None:
    """
    Очищает excel файл
    """
    doc = openpyxl.open(filename='data/database.xlsx')
    doc.remove_sheet(doc.worksheets[0])
    doc.save(filename='data/database.xlsx')


def get_users_id() -> list:
    """
    Возвращает список id всех инициаторов платежей
    """
    db_connection = psycopg2.connect(DB_URI, sslmode="require")
    db_object = db_connection.cursor()

    db_object.execute(
        "SELECT DISTINCT id FROM register"
    )

    result = db_object.fetchall()
    return result


def get_files_id(user_id) -> list:
    """
    Возвращает список всех файлов с сервера Telegram
    result[0] = Название
    result[1] = unic_id из базы данных

    user_id - id инициатора
    """
    db_connection = psycopg2.connect(DB_URI, sslmode="require")
    db_object = db_connection.cursor()

    db_object.execute(
        f"SELECT basis_of_payment, callback_id FROM register WHERE (id = {user_id}) AND (file_id NOT LIKE '%nothing%')"
    )

    result = db_object.fetchall()
    return result
