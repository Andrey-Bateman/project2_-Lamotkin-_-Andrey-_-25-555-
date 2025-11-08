from typing import Any, Dict, List


def create_table(metadata: Dict[str, Any],
 table_name: str,
 columns: List[str]
) -> Dict[str, Any]:
    if "tables" not in metadata:
        metadata["tables"] = {}
    if table_name in metadata["tables"]:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata
    full_columns = ["ID:int"] + columns
    valid_types = {"int", "str", "bool"}
    for col in columns:
        parts = col.split(":")
        if len(parts) != 2 or parts[1] not in valid_types or not parts[0]:
            print(
                f'Некорректное значение: {col}. '
                f'Поддерживаемые типы: int, str, bool. '
                f'Формат: имя:тип.'
            )
            return metadata
    metadata["tables"][table_name] = {"columns": full_columns}
    print(
    f'Таблица "{table_name}" успешно создана '
    f'со столбцами: {", ".join(full_columns)}')
    return metadata

def drop_table(metadata: Dict[str, Any], table_name: str) -> Dict[str, Any]:
    if table_name not in metadata.get("tables", {}):
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    del metadata["tables"][table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata: Dict[str, Any]) -> None:
    """Показывает список таблиц."""
    tables = metadata.get("tables", {})
    if not tables:
        print('- (нет таблиц)')
    else:
        print('- ' + '\n- '.join(sorted(tables.keys())))
