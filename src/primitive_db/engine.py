import shlex

from src.primitive_db.core import create_table, drop_table, list_tables
from src.primitive_db.utils import load_metadata, save_metadata

METADATA_FILE = "db_meta.json"

def print_help():
    """Prints the help message."""
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип>"
         " <столбец2:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    metadata = load_metadata(METADATA_FILE)
    print_help()
    while True:
        user_input = input(">>>Введите команду: ").strip()
        if not user_input:
            print("Некорректное значение: (пустая команда).Попробуйте снова.")
            continue
        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Некорректное значение: {user_input}. {e}. Попробуйте снова.")
            continue
        command = args[0].lower()
        if command == "exit":
            print("Выход из программы.")
            break
        elif command == "help":
            print_help()
        elif command == "create_table":
            if len(args) < 2:
                print("Некорректное значение: недостаточно аргументов."
                       " Попробуйте снова.")
                continue
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata(METADATA_FILE, metadata)
        elif command == "drop_table":
            if len(args) < 2:
                print("Некорректное значение: недостаточно аргументов."
                      " Попробуйте снова.")
                continue
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata(METADATA_FILE, metadata)
        elif command == "list_tables":
            list_tables(metadata)
        else:
            print(f'Функции "{command}" нет. Попробуйте снова.')
