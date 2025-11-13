import json
import os
from typing import Dict, Any, List

def load_metadata(filepath="db_meta.json"):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}  
    return {}  

def save_metadata(filepath, metadata):
    dir_path = os.path.dirname(filepath)
    if dir_path and dir_path != '.':  
        os.makedirs(dir_path, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
import json
import os

def load_table_data(table_name):
    file_path = f"data/{table_name}.json"
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return []  
        except (json.JSONDecodeError, ValueError):
            return []  
    return []  
def save_table_data(table_name, data):
    file_path = f"data/{table_name}.json"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)  
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
