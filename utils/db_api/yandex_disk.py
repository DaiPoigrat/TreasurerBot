import logging

from data.config import YADISK_TOKEN
import yadisk


def upload_register():
    """
    Загружает реестр на диск
    """
    try:
        disk = yadisk.YaDisk(token=YADISK_TOKEN)
        disk.remove(path='register.xlsx')
        disk.upload(path_or_file='data/register.xlsx', dst_path='register.xlsx')
        logging.info(msg='Реестр успешно отправлен на диск')
    except Exception as err:
        logging.exception(err)


def download_register():
    """
    Обновляет содержимое реестра на сервере с диска
    """
    try:
        disk = yadisk.YaDisk(token=YADISK_TOKEN)
        disk.download(src_path='register.xlsx', path_or_file='data/register.xlsx')
        logging.info(msg='Реестр успешно обновлен с диска')
    except Exception as err:
        logging.exception(err)
