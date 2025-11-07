import prompt

def welcome():
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    name = prompt.string('Как твое имя? ')
    print(f'Приет , {name}!')
    while True:
        command = prompt.string('Введите команду: ')
        if command == 'exit':
            print('Выход из программы')
            break
        elif command == 'help':
            print('<command> exit - выйти из программы')
            print('<command> help - справочная информация')
        else:
            print('Неизвестная команда. Введите help для справки.')

