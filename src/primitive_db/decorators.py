import functools
import time
from typing import Callable, Any
def handle_db_errors(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец '{e}' не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper
def confirm_action(action_name: str):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            confirm = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()
            if confirm != 'y':
                print(f"Операция '{action_name}' отменена.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        end = time.monotonic()
        print(f"Функция '{func.__name__}' выполнилась за {end - start:.3f} секунд.")
        return result
    return wrapper

def create_cacher():
    cache = {}  

    def cache_result(key: str, value_func: Callable) -> Any:
        if key in cache:
            print(f"Результат для ключа '{key}' взят из кэша.")
            return cache[key]
        result = value_func()
        cache[key] = result
        print(f"Результат для ключа '{key}' вычислен и сохранён в кэше.")
        return result
    return cache_result
