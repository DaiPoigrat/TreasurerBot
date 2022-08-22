import psycopg2
import logging
import openpyxl
from aiogram.types import InputFile

from data.config import DB_URI

titles = ['Дата поступления', 'Инициатор платежа', 'Основание платежа', 'id документа', 'Сумма платежа',
          'Размер оплаты', 'Получатель', 'Назначение', 'Крайний срок оплаты']


def add_record(data: list) -> None:
    """
    Создает запить в базе данных
    """
    try:
        db_connection = psycopg2.connect(DB_URI, sslmode="require")
        db_object = db_connection.cursor()

        db_object.execute(
            "INSERT INTO register(id, date_of_application, payment_iniciator, basis_of_payment, file_id, payment_sum, payment_amount, payment_recipient, purpose_of_payment, payment_deadline) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]))
        db_connection.commit()
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
            "SELECT date_of_application, payment_iniciator, basis_of_payment, file_id, payment_sum, payment_amount, payment_recipient, purpose_of_payment, payment_deadline FROM register"
        )

        result = db_object.fetchall()

        doc = openpyxl.open(filename='data/register.xlsx')
        doc.create_sheet(title='Заявки', index=0)
        sheet = doc.worksheets[0]
        sheet.append(titles)

        for row in result:
            sheet.append([str(item).rstrip() for item in row])

        doc.save(filename='data/register.xlsx')
    except Exception as err:
        logging.exception(err)


def drop_excel() -> None:
    """
    Очищает excel файл
    """
    doc = openpyxl.open(filename='data/register.xlsx')
    doc.remove_sheet(doc.worksheets[0])
    doc.save(filename='data/register.xlsx')


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


def recreate_table() -> None:
    db_connection = psycopg2.connect(DB_URI, sslmode="require")
    db_object = db_connection.cursor()
    db_object.execute(
        """
        create table register
        (
            id                  integer   not null,
            date_of_application char(50)  not null,
            payment_iniciator   char(300) not null,
            basis_of_payment    char(300) not null,
            payment_sum         integer   not null,
            payment_amount      char(10)  not null,
            payment_recipient   char(300) not null,
            purpose_of_payment  char(300) not null,
            payment_deadline    char(20)  not null,
            file_id             char(300) not null,
            callback_id         integer generated always as identity
        );
        comment on column register.id is 'id юзера в телеге';

        comment on column register.date_of_application is 'дата получения заявки';
        
        comment on column register.payment_iniciator is 'инициатор платежа';
        
        comment on column register.basis_of_payment is 'основание платежа (текст или название дока)';
        
        comment on column register.payment_sum is 'сумма платежа';
        
        comment on column register.payment_amount is 'размер оплаты';
        
        comment on column register.payment_recipient is 'получатель';
        
        comment on column register.purpose_of_payment is 'назначение платежа';
        
        comment on column register.payment_deadline is 'крайний срок оплаты';
        
        comment on column register.file_id is 'id файла или 0, если текстовое описание';
        
        alter table register
            owner to tqwsruaobvphad;
        """
    )



