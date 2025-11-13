from typing import Dict, Any, List
from .utils import load_metadata
from src.primitive_db.utils import load_table_data

def create_table(metadata: Dict[str, Any], table_name: str, columns: List[str]) -> Dict[str, Any]:
    if "tables" not in metadata:
        metadata["tables"] = {}
    if table_name in metadata["tables"]:
        raise ValueError(f'Таблица "{table_name}" уже существует.')
    table_columns = {}
    valid_types = {"int", "str", "bool"}
    for col in columns:
        parts = col.split(":")
        if len(parts) != 2 or parts[1] not in valid_types or not parts[0]:
            raise ValueError(
                f'Некорректное значение: {col}. '
                f'Поддерживаемые типы: int, str, bool. '
                f'Формат: имя:тип.'
            )
        table_columns[parts[0]] = parts[1]
    
    if "ID" not in table_columns:
        table_columns["ID"] = "int"
    metadata["tables"][table_name] = {"columns": table_columns}
    return metadata

def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    if table_name not in metadata.get("tables", {}):
        raise ValueError(f'Таблица "{table_name}" не существует.')
    del metadata["tables"][table_name]
    return metadata

def list_tables(metadata: Dict[str, Any]) -> None:
    tables = metadata.get("tables", {})
    if not tables:
        print('- (нет таблиц)')
    else:
        print('- ' + '\n- '.join(sorted(tables.keys())))

def validate_value(value: str, col_type: str) -> Any:
    if col_type == "int":
        try:
            return int(value)
        except ValueError:
            raise ValueError(f'Значение "{value}" не int.')
    elif col_type == "bool":
        lower_val = value.lower()
        if lower_val in ("true", "1", "yes", "да"):
            return True
        if lower_val in ("false", "0", "no", "нет"):
            return False
        raise ValueError(f'Значение "{value}" не bool.')
    elif col_type == "str":
        return value
    raise ValueError(f'Неизвестный тип {col_type}.')

def insert(metadata, table_name, values):
   
    if not metadata or table_name not in metadata:
        raise ValueError(f"Таблица '{table_name}' не существует.")
    
    columns = metadata[table_name]['columns']  
    if len(values) != len(columns) - 1:  
        raise ValueError(f"Ожидается {len(columns) - 1} значений, получено {len(values)}.")
    
    
    for i, (col_name, col_type) in enumerate(columns[1:], 1):  
        val = values[i-1]
        if col_type == 'int' and not isinstance(val, int):
            try:
                val = int(val)
            except ValueError:
                raise ValueError(f"Значение '{val}' для '{col_name}' должно быть int.")
        elif col_type == 'str' and not isinstance(val, str):
            val = str(val)
        elif col_type == 'bool' and not isinstance(val, bool):
            if val.lower() in ('true', '1', 'yes'):
                val = True
            elif val.lower() in ('false', '0', 'no'):
                val = False
            else:
                raise ValueError(f"Значение '{val}' для '{col_name}' должно быть bool.")
        values[i-1] = val  
    
    table_data = load_table_data(table_name)
    
    if table_data:
        new_id = max(row['ID'] for row in table_data) + 1
    else:
        new_id = 1
    
    new_row = {'ID': new_id}
    for i, (col_name, _) in enumerate(columns[1:], 1):
        new_row[col_name] = values[i-1]
    
    table_data.append(new_row)
    return table_data  

def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data
    return [row for row in table_data if all(row.get(key) == value for key, value in where_clause.items())]

def update(table_data, set_clause, where_clause):
    updated_rows = [row for row in table_data if all(row.get(key) == value for key, value in where_clause.items())]
    if not updated_rows:
        raise ValueError("Записи для обновления не найдены.")
    
    for row in updated_rows:
        for key, value in set_clause.items():
            row[key] = value
    
    return table_data  
def delete(table_data, where_clause):
    initial_count = len(table_data)
    table_data[:] = [row for row in table_data if not all(row.get(key) == value for key, value in where_clause.items())]
    if len(table_data) == initial_count:
        raise ValueError("Записи для удаления не найдены.")
    return table_data  
def info(metadata, table_name):
    if table_name not in metadata.get('tables', {}):
        raise ValueError(f"Таблица '{table_name}' не существует.")
    columns = metadata['tables'][table_name]['columns']
    col_order = ['ID'] + [col for col in columns if col != 'ID']
    col_str = ', '.join(f"{col}:{columns[col]}" for col in col_order)
    data = load_table_data(table_name)
    return f"Таблица: {table_name}\nСтолбцы: {col_str}\nКоличество записей: {len(data)}"
