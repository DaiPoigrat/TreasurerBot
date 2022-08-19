# скрипт создания реестра
import datetime
import openpyxl
import typing

# ключи доступа к файлам словаря данных заявки
from utils.db_api.db_manage import add_record

dict_keys = ['user_id', 'file_name', 'file_id', 'payment_sum', 'payment_amount', 'payment_recipient',
             'purpose_of_payment', 'payment_deadline']

titles = ['Дата поступления', 'Инициатор платежа', 'Основание платежа', 'Сумма платежа', 'Размер оплаты',
          'Получатель', 'Назначение', 'Крайний срок оплаты']


def get_active_registry() -> str:
    """
    Возвращает название активного реестра
    """
    with open('data/active_registry', 'r') as file:
        return file.readline()


def set_active_registry(new_active: str) -> None:
    """
    Меняет активный реест
    """
    with open('data/active_registry', 'w') as file:
        file.write(f'{new_active}')


# получаем дату в нужном формате
def get_date() -> str:
    """
    Влзвращает текущую дату и время
    д-м-гггг ч-м-с
    """
    # получаем текущее время
    time_object = datetime.datetime.now()

    # и выделяем день, месяц и год
    today = [str(time_object.day), str(time_object.month), str(time_object.year)]
    # час, минута, секунда
    hms = [str(time_object.hour), str(time_object.minute), str(time_object.second)]
    return '-'.join(today) + ' ' + ':'.join(hms)


def create_book(name: str) -> None:
    """
    Создает реестр в формате excel
    """
    # создание книги в excel
    new_registry = openpyxl.Workbook()
    # удаление таблицы Sheet по-умолчанию
    new_registry.remove(new_registry.active)

    sheet = new_registry.create_sheet(title='Заявки')

    sheet.append(titles)

    new_registry.save(filename=f'registries/{name}')


def create_data_record(data: dict, name: str) -> None:
    """
    Создает новую запись в реестре
    """
    # active_registry = get_active_registry()
    # # открываем книгу с текущей датой создания
    # book = openpyxl.open(filename=f'registries/{active_registry}')
    # sheet = book.worksheets[0]

    # собираем данные в список, устанавляивая типы данных
    data_set = [
        int(data[dict_keys[0]]),
        get_date(),
        name,
        data[dict_keys[1]],
        data[dict_keys[2]],
        int(data[dict_keys[3]]),
        data[dict_keys[4]],
        data[dict_keys[5]],
        data[dict_keys[6]],
        data[dict_keys[7]]
    ]

    add_record(data=data_set)

    # # записываем в строку таблицы
    # sheet.append(data_set)
    # # сохраняем результат
    # book.save(filename=f'registries/{active_registry}')


# вспомогательные функции
def writeBuffer(inf: str) -> None:
    """
    Запись данных в буфер
    """
    with open('data/buffer', 'w') as buffer:
        buffer.write(inf)

    buffer.close()


def readBuffer() -> str:
    """
    Чтение из буфера
    """
    with open('data/buffer', 'r') as buffer:
        inf = buffer.readline()
        buffer.close()
        return inf
