Управление базами данных 
После запуска кода  ааодите следующие команды:


- `create_table <имя> <столбец1:тип> ...` — создать таблицу (типы: int, str, bool; ID добавляется автоматически).
- `list_tables` — список таблиц.
- `drop_table <имя>` — удалить таблицу.
- `help` — справка.
- `exit` — выход.

Пример:
>>>Введите команду: create_table магазин продажи:bool цена:int

Таблица "магазин" успешно создана со столбцами: ID:int, продажи:bool, цена:int

>>>Введите команду: list_tables

- магазин

>>>Введите команду: exit

 Демо работы 
https://asciinema.org/a/EpT125IvFH5jeXRZtOHsWfVGF

 CRUD-операции

Команды:

- `insert into <table> values (<val1>, <val2>, ...)` – добавить запись (ID генерируется автоматически).

- `select from <table> [where <col> = <val>]` – выбрать все или по условию.

- `update <table> set <col> = <new_val> where <col> = <val>` – обновить.

- `delete from <table> where <col> = <val>` – удалить.

 Демо работы
https://asciinema.org/a/JNQeJmHEBfAuV8gtlTyImOjLe

 Декораторы и замыкания

Проект улучшен с помощью декораторов для обработки ошибок (@handle_db_errors), подтверждения действий (@confirm_action), замера времени (log_time) и замыкания для кэширования в select.

Новые возможности:

- Автоматическая обработка ошибок без дублирования кода.

- Подтверждение для удаления (y/n).

- Замер времени выполнения insert/select.

- Кэширование результатов select (повторные запросы быстрее).

Демо работы

https://asciinema.org/a/zxrNcW5zBhnPq4KRsGU7ncUz7
