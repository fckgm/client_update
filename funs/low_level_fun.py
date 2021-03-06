import os
import subprocess
import sys
import time
import winreg as reg
import platform
import shutil
from ctypes import windll
from subprocess import run, PIPE, Popen
from datetime import datetime

from bin.values import *
import logging


# Проверяет, запущенн ли client от имени администратора
def is_admin():
    try:  # Пытаемся вернуть True admin-mode
        return windll.shell32.IsUserAnAdmin()
    except:  # Иначе возвращаем False
        return False


# Возвращает список аргументов коммандной строки
def get_argv_list(argv):
    if argv[1:]:  # Если есть аргументы коммандной строки
        argv_list = argv[1:]  # Исключаем первый элемент

        return argv_list

    else:  # Если нет, возвращаем пустой список
        return []


# Возвращает, требуется ли загружать loader client-у
def need_init_loader(argv):
    argv_list = get_argv_list(argv)

    if DONT_NEED_INIT_LOADER_ARG in argv_list:  # Если есть флаг в списке
        return False
    else:  # Иначе
        return True


# Первичная инициализация ключей реестра с возвратом ключа
def first_init_reg_keys():
    k = reg.CreateKeyEx(reg.HKEY_CURRENT_USER, REG_ROOT_PATH, 0, reg.KEY_ALL_ACCESS)

    reg.SetValueEx(k, REG_VERSION_KEY, 0, reg.REG_SZ, APP_VERSION)  # Версия программы

    return k


# Возвращает словарь реестра программы
def get_reg_dict():
    try:  # Пытаемя открыть раздел еестра
        k = reg.OpenKey(reg.HKEY_CURRENT_USER, REG_ROOT_PATH, 0, reg.KEY_ALL_ACCESS)

    except FileNotFoundError:  # Если раздела не существует
        k = first_init_reg_keys()  # Проводим первичную инициализацию

    count_keys = reg.QueryInfoKey(k)[1]  # Колличество ключей раздела реестра

    reg_dict = {}  # Словаь ключей реестра
    for index in range(count_keys):  # Проходим по ключам
        key, value, types = reg.EnumValue(k, index)
        reg_dict[key] = value  # Пишем ключ - значение

    return reg_dict


# Устанавливает значение в реестр (по пути REG_ROOT)
def set_reg_key(key, value):
    k = reg.OpenKey(reg.HKEY_CURRENT_USER, REG_ROOT_PATH, 0, reg.KEY_ALL_ACCESS)

    reg.SetValueEx(k, key, 0, reg.REG_SZ, value)  # Устанавливаем значение в реестр


# # Устанавливает время последнего запуска программы в реестр
# def set_last_run():
#     now = str(time.time())  # Получаем текущее время (с начала эпохи)
#     set_reg_key(REG_LAST_RUN_KEY, now)  # Устанавливаем в реестр


# Устанавливает время последнего сбора информации о ККМ в реестр
def set_kkm_data_last_run():
    now = str(time.time())  # Получаем текущее время (с начала эпохи)
    set_reg_key(REG_LAST_RUN_KKM_DATA_KEY, now)  # Устанавливаем в реестр


# Устанавливает время последнего сбора информации о дисках и бекапах в реестр
def set_disk_usage_last_run():
    now = str(time.time())  # Получаем текущее время (с начала эпохи)
    set_reg_key(REG_LAST_RUN_DISK_USAGE, now)  # Устанавливаем в реестр


# Запускает "первичныe скрипты"
def run_first_scripts():
    try:
        first_popen()  # Скрипты без ожидания завершения
    except FileNotFoundError:
        pass
    try:
        first_run()  # Скрипты с ожиданием завершения
    except FileNotFoundError:
        pass
    try:
        run_once()  # RunOnce скрипты
    except FileNotFoundError:
        pass

    try:
        if os.path.exists('_migrate_vnc_lite'):
            with open('_migrate_vnc_lite') as file:
                address = file.read().strip()

            migrate_vnc_lite(address)
            os.remove('_migrate_vnc_lite')
    except Exception:
        pass

    try:
        urgent_tasks()
    except Exception:
        pass

    try:
        moveFiles()
        os.rmdir(moveFrom, dir_fd=None)
    except Exception:
        pass


# TODO Срочные задачи
def urgent_tasks():
    try:
        clear_1c()
    except Exception:
        pass

    try:
        taskkill_bcm()
    except Exception:
        pass


# TODO Срочно
moveFrom = Path(__file__).parent.joinpath('Move')
moveTo = r'C:\Sphinx'


# перемещает файлы сфинкса
def moveFiles():
    if not os.path.exists(moveTo):
        shutil.rmtree(moveFrom)
        return

    needToMove = os.listdir(moveFrom)
    if not needToMove:
        os.rmdir(moveFrom, dir_fd=None)
        return

    res = subprocess.run('net stop SphinxSearch', stdin=PIPE, stderr=PIPE, stdout=PIPE)
    if res.stderr:
        return

    for file in needToMove:
        try:
            path_from = os.path.join(moveFrom, file)
            path_to = os.path.join(moveTo, file)
            shutil.move(path_from, path_to, copy_function=shutil.copy2)
        except Exception:
            pass

    res = subprocess.run('net start SphinxSearch', stdin=PIPE, stderr=PIPE, stdout=PIPE)
    if res.stderr:
        pass  # Это хуёво


# Завершает процессы BMC
def taskkill_bcm():
    if os.path.exists('_taskkill_bmc'):
        subprocess.run(
            'taskkill /f /im BMCClient.exe', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL)
        subprocess.run(
            'taskkill /f /im tvnserver.exe', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL)

        # HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
        # %userprofile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
        try:
            startup_path = Path().home().joinpath(r'AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
            startup_listdir = os.listdir(startup_path)
            for name in startup_listdir:
                if 'bmc' in name.lower():
                    path = startup_path.joinpath(name)
                    os.remove(path)
        except Exception:
            pass

        regpath = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        try:
            k_user = reg.OpenKey(reg.HKEY_CURRENT_USER, regpath, 0, reg.KEY_ALL_ACCESS)
            count = reg.QueryInfoKey(k_user)[1]
            for index in range(count):  # Проходим по ключам
                key, value, types = reg.EnumValue(k_user, index)

                if 'bmc' in value.lower():
                    reg.DeleteValue(k_user, key)

        except Exception:
            pass

        try:
            k_machine = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, regpath, 0, reg.KEY_ALL_ACCESS)
            count = reg.QueryInfoKey(k_machine)[1]
            for index in range(count):  # Проходим по ключам
                key, value, types = reg.EnumValue(k_machine, index)

                if 'bmc' in value.lower():
                    reg.DeleteValue(k_machine, key)

        except Exception:
            pass

        os.remove('_taskkill_bmc')


# TODO Срочно
# Меняет адрес VNC Lite
def migrate_vnc_lite(address: str):
    path = r'SOFTWARE\NevisVNCLite\settings'
    try:
        k = reg.OpenKey(reg.HKEY_CURRENT_USER, path, 0, reg.KEY_ALL_ACCESS)
    except FileNotFoundError:
        return

    reg.SetValueEx(k, 'host', 0, reg.REG_SZ, address)


# TODO Срочно
# Запускает чистку 1С
def clear_1c():
    if os.path.exists('_run_1c_clear'):
        path_to_clear_1c = os.path.join(ROOT_PATH, SOFT_DIR_NAME, CLEAR_1C_NAME)

        run(path_to_clear_1c, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        os.remove('_run_1c_clear')


# Запускает первичные скрипты и дожидается завершения
def first_run(dirname=None):
    if not dirname:  # Если директория не передана
        dirname = FIRST_RUN_DIR_NAME  # Стандартная директория first run
        listdir = os.listdir(dirname)  # Список файлов в _first_run
    else:  # Если передана
        listdir = os.listdir(dirname)  # Список файлов в переданной директории
    # Список скриптов в директории
    listscripts = [file for file in listdir if file.endswith('.py') or file.endswith('.pyw')]

    for script in listscripts:  # Проходим по списку скриптов
        if script.endswith('.py'):  # Стандартный интропретатор
            run([PATH_TO_PYTHON, os.path.join(dirname, script)], shell=True,
                stdout=PIPE, stderr=PIPE, stdin=PIPE)

        if script.endswith('pyw'):  # No-Console
            run([PATH_TO_PYTHON_NO_CONSOLE, os.path.join(dirname, script)], shell=True,
                stdout=PIPE, stderr=PIPE, stdin=PIPE)


# Запускает первичные скрипты и продолжает работу
def first_popen():
    listdir = os.listdir(FIRST_POPEN_DIR_NAME)  # Список файлов в _first_popen
    # Список скриптов в директории
    listscripts = [file for file in listdir if file.endswith('.py') or file.endswith('.pyw')]

    for script in listscripts:
        if script.endswith('.py'):  # Стандартный интропретатор
            Popen([PATH_TO_PYTHON, os.path.join(FIRST_POPEN_DIR_NAME, script)], shell=True,
                  stdout=PIPE, stderr=PIPE, stdin=PIPE)

        if script.endswith('pyw'):  # No-Console
            Popen([PATH_TO_PYTHON_NO_CONSOLE, os.path.join(FIRST_POPEN_DIR_NAME, script)], shell=True,
                  stdout=PIPE, stderr=PIPE, stdin=PIPE)


# Запускает скрипт единожды
def run_once():
    first_run(RUN_ONCE_DIR_NAME)  # Запускаем скрипты в _run_once
    time.sleep(0.5)  # Чуть-чуть ждём

    shutil.rmtree(RUN_ONCE_DIR_NAME)  # Удаляем директорию


# Проверяет, не содержит ли путь к клиенту пробельных символов
def path_to_client_with_space():
    path_to_script = sys.argv[0]  # Пусть к клиенту

    if ' ' in path_to_script:  # Если есть пробелы в пути
        return True
    else:
        return False


# Возвращяет корректный путь до клиента (экранирование пробелов в пути)
def get_correct_path():
    if path_to_client_with_space():  # Если в пути есть пробелы
        path_to_script = f'"{sys.argv[0]}"'  # Пишем в кавычках
    else:
        path_to_script = sys.argv[0]  # Возвращаем как есть

    return path_to_script


# Устанавливет библиотеку(ки)
def library_install(lib):
    if isinstance(lib, str):  # Если передана одна библиотека
        run([sys.executable, os.path.join(os.getcwd(), SCRIPTS_DIR_NAME, INSTALLER_LIBRARY_MODULE_NAME), lib])
    elif any((isinstance(lib, list), isinstance(lib, tuple))):  # Если несколько библиотек
        lib = ' '.join(lib)  # Объединяем по пробелу
        run([sys.executable, os.path.join(os.getcwd(), SCRIPTS_DIR_NAME, INSTALLER_LIBRARY_MODULE_NAME), lib])


# Создаёт директорию runtime
def mkdrir_runtime():
    os.mkdir(os.path.join(ROOT_PATH, RUNTIME_DIR_NAME))


# Инициализирует logger
def init_logger():
    try:
        fh = logging.FileHandler(LOG_FILE_PATH, 'a', ENCODING_APP)  # Файл лога
    except FileNotFoundError:  # Если нет директории runtime
        mkdrir_runtime()  # Создаём папку runtime
        fh = logging.FileHandler(LOG_FILE_PATH, 'a', ENCODING_APP)  # Файл лога
    str_format = '[%(asctime)s]: %(levelname)s - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) ' \
                 '=> %(message)s'  # Формат вывода
    date_format = '%X %d/%m/%y'  # Формат даты/времени
    formatter = logging.Formatter(fmt=str_format, datefmt=date_format)
    fh.setFormatter(formatter)  # Устанавливаем форматирование

    return fh  # Возвращаем настроенный логгер


# Возвращает объект logger-a
def get_logger(name):
    logger = logging.getLogger(name)  # Инициализируем объект логгера с именем программы
    logger.setLevel(logging.INFO)  # Уровень логгирования
    logger.addHandler(init_logger())  # Добавляем

    return logger
