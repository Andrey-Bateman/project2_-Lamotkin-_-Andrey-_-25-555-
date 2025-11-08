import json
from typing import Any, Dict


def load_metadata(filepath: str) -> Dict[str, Any]:
    """Загружает метаданные из JSON. Если файл не найден, возвращает {}."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tables": {}}

def save_metadata(filepath: str, data: Dict[str, Any]) -> None:
    """Сохраняет метаданные в JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
