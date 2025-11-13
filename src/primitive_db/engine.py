import shlex
import re  
from prettytable import PrettyTable
from .core import insert, select, update, delete  
from .utils import load_table_data, save_table_data, load_metadata, save_metadata
from typing import Dict, Any, List

def print_help():
    print("create table <имя_таблицы> (<столбец1:тип1>, <столбец2:тип2>, ...) - создать таблицу.")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> [where <столбец> = <значение>] - прочитать записи.")
    print("<command> update <имя_таблицы> set <столбец> = <новое_значение> where <столбец> = <значение> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> list_tables - список таблиц.")
    print("<command> drop table <имя_таблицы> - удалить таблицу.")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")

def parse_where(where_str):
    """Парсит 'col = value' в {'col': value}."""
    if not where_str:
        return None
    match = re.match(r'(\w+)\s*=\s*(.+)', where_str.strip())
    if not match:
        raise ValueError("Неверный формат where: ожидается 'col = value'.")
    col = match.group(1).strip()
    val_str = match.group(2).strip()
    if val_str.startswith('"') and val_str.endswith('"'):
        value = val_str[1:-1]
    elif val_str.lower() in ('true', 'false'):
        value = val_str.lower() == 'true'
    else:
        try:
            value = int(val_str)
        except ValueError:
            value = val_str  
    return {col: value}

def parse_set(set_str):
    """Парсит 'col = value' в {'col': value}."""
    return parse_where(set_str)  

def parse_schema(schema_str):
    """Парсит '(ID:int, name:str, ...)' в [('ID', 'int'), ...]."""
    if not schema_str.startswith('(') or not schema_str.endswith(')'):
        raise ValueError("Схема должна быть в скобках: (col:type, ...)")
    inner = schema_str[1:-1].strip()
    parts = [p.strip() for p in inner.split(',')]
    columns = []
    for part in parts:
        if ':' not in part:
            raise ValueError(f"Неверный формат столбца: {part} (ожидается col:type)")
        name, typ = [x.strip() for x in part.split(':', 1)]
        columns.append((name, typ))
    return columns

def run():
    metadata = load_metadata("db_meta.json")
    if metadata is None:
        metadata = {}
    print("database")
    print_help()
    while True:
        user_input = input(">>> Введите команду: ").strip()
        if not user_input:
            continue
        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f"Ошибка парсинга: {e}")
            continue
        if not args:
            continue
        command = args[0].lower()
        try:
            if command == "exit":
                break
            elif command == "help":
                print_help()
            elif command == "create" and len(args) > 2 and args[1] == "table":
                if len(args) < 4:
                    print("Использование: create table <имя_таблицы> (col1:type1, col2:type2, ...)")
                    continue
                table_name = args[2]
                if table_name in metadata:
                    print(f"Таблица '{table_name}' уже существует.")
                    continue
                schema_str = ' '.join(args[3:])
                columns = parse_schema(schema_str)
                metadata[table_name] = {'columns': columns}
                save_metadata("db_meta.json", metadata)
                print(f"Таблица '{table_name}' создана.")
            elif command == "drop" and len(args) > 2 and args[1] == "table":
                table_name = args[2]
                if table_name in metadata:
                    del metadata[table_name]
                    save_metadata("db_meta.json", metadata)
                    print(f"Таблица '{table_name}' удалена.")
                else:
                    print(f"Таблица '{table_name}' не существует.")
            elif command == "list_tables":
                print("Доступные таблицы:", list(metadata.keys()) if metadata else [])
            elif command == "info" and len(args) == 2:
                table_name = args[1]
                if table_name in metadata:
                    columns = metadata[table_name]['columns']
                    col_info = ', '.join([f"{name}:{typ}" for name, typ in columns])
                    table_data = load_table_data(table_name)
                    print(f"Таблица: {table_name}")
                    print(f"Столбцы: {col_info}")
                    print(f"Количество записей: {len(table_data)}")
                else:
                    print(f"Таблица '{table_name}' не существует.")
            elif command == "insert" and len(args) >= 5 and args[1] == "into" and args[3] == "values":
                table_name = args[2]
                if table_name not in metadata:
                    print(f"Таблица '{table_name}' не существует.")
                    continue
                values_str = ' '.join(args[4:])
                if not (values_str.startswith('(') and values_str.endswith(')')):
                    print("Значения должны быть в скобках: values (val1, val2, ...)")
                    continue
                values_inner = values_str[1:-1]
                values = re.split(r',\s*(?=(?:[^"]*"[^"]*")*[^"]*$)', values_inner)
                values = [v.strip().strip('"') for v in values] 
                try:
                    table_data = insert(metadata, table_name, values)
                    save_table_data(table_name, table_data)
                    new_id = table_data[-1]['ID'] if table_data else 1
                    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
                except Exception as e:
                    print(f"Ошибка вставки: {e}")
            elif command == "select" and len(args) >= 3 and args[1] == "from":
                table_name = args[2]
                if table_name not in metadata:
                    print(f"Таблица '{table_name}' не существует.")
                    continue
                where_str = None
                where_idx = -1
                if len(args) > 3 and args[3] == "where":
                    where_idx = args.index("where")
                    where_str = ' '.join(args[where_idx+1:])
                table_data = load_table_data(table_name)
                where_clause = parse_where(where_str) if where_str else None
                result = select(table_data, where_clause)
                if result:
                    pt = PrettyTable()
                    headers = list(result[0].keys()) if result else []
                    pt.field_names = headers
                    for row in result:
                        pt.add_row([row.get(h, '') for h in headers])
                    print(pt)
                else:
                    print("Нет данных.")
            elif command == "update" and len(args) >= 5 and args[2] == "set":
                table_name = args[1]
                if table_name not in metadata:
                    print(f"Таблица '{table_name}' не существует.")
                    continue
                set_idx = args.index("set")
                where_str = None
                if "where" in args:
                    where_idx = args.index("where")
                    set_str = ' '.join(args[set_idx+1:where_idx])
                    where_str = ' '.join(args[where_idx+1:])
                else:
                    set_str = ' '.join(args[set_idx+1:])
                set_clause = parse_set(set_str)
                where_clause = parse_where(where_str)
                if not where_clause:
                    print("Where условие обязательно для update.")
                    continue
                table_data = load_table_data(table_name)
                try:
                    table_data = update(table_data, set_clause, where_clause)
                    save_table_data(table_name, table_data)
                    print(f'Запись с ID=1 в таблице "{table_name}" успешно обновлена.')  
                except Exception as e:
                    print(f"Ошибка обновления: {e}")
            elif command == "delete" and len(args) >= 4 and args[1] == "from":
                table_name = args[2]
                if table_name not in metadata:
                    print(f"Таблица '{table_name}' не существует.")
                    continue
                if "where" not in args:
                    print("Where условие обязательно для delete.")
                    continue
                where_idx = args.index("where")
                where_str = ' '.join(args[where_idx+1:])
                where_clause = parse_where(where_str)
                table_data = load_table_data(table_name)
                try:
                    table_data = delete(table_data, where_clause)
                    save_table_data(table_name, table_data)
                    print(f'Запись с ID=1 успешно удалена из таблицы "{table_name}".')  
                except Exception as e:
                    print(f"Ошибка удаления: {e}")
            else:
                print("Неизвестная команда. Введите 'help' для справки.")
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    run()
