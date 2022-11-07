COMMANDS = {}  # словник команд
CONTACTS = {}  # словник контактів


def command(*args):
    """ф-ція декоратор команд. 
    на вхід приймає аргумент яку сприймаємо як ф-цію
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        for x in args:
            # Нашо, якшо немає нечутливості до регістру?
            COMMANDS[x.lower()] = inner
        return inner
    return wrapper


def input_error(error_message_dict):
    """ф-ція декоратор який вловлює похибки
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            # пробуємо передати аргументи в ф-цію
            try:
                return func(*args, **kwargs)
            # якшо вловлюємо похибку і передаємо в змінну
            except Exception as err:
                if err in error_message_dict.keys():  # якшо похибка є ключем в словнику
                    print(error_message_dict[err])  # видаємо похибку
                    return err
                raise err  # якшо якась невідома похибка, передаємо в змінну аби вивести
        return inner
    return wrapper


@command("good bye", "exit", "close")
@input_error({TypeError: "This command doesn't take arguments"})
def goodbye():
    """ф-ція закінчення роботи якшо буде передана одна з команд
    """
    print("This is the end")
    exit()


@command("hello")
@input_error({TypeError: "This command doesn't take arguments"})
def hello():
    """ф-ція привітання. Видає повідовлення при запиті 
    """
    return "How can I help you?"


@command(".")
@input_error({TypeError: "This command doesn't take arguments"})
def nothing():
    exit()


@command('add')
@input_error("Enter name and number")
def add(name, number):
    """ф-ція запису в словник інформації
    """
    CONTACTS[name] = number
    return ""


@command('show all')
@input_error({TypeError: "This command doesn't take arguments"})
def show_all():
    """ф-ція виводу записаної інформації
    """
    return CONTACTS


@command('phone')
@input_error({TypeError: "This command takes only Name arguments"})
def phone(name):
    """ф-ція запиту №телефону словнику за ім"ям
    """
    return CONTACTS[name]


@command('change')
@input_error({
    IndexError: "Non-existing name",
    TypeError: "This command takes only Name arguments"
})
def change(name, number):
    """ф-ція команди "зміни". вносить зміну в значення словнику по ключу
    """
    CONTACTS[name] = number
    return ""


def parse_command(string: str):
    """ф-ція яка допогая отримати команду в звичайному варіант. Використовуємо звичайний пробіл
    """
    for command in COMMANDS.keys():
        if string.startswith(command):
            return command, string[len(command):].split()


def main():
    """Головна ф-ція.
    Запускає нескінченний цикл, вихід з якого можно виконати за командами
    """
    while True:
        # запит на введеня інформації
        string = input("Command: ")
        # умова не чутливості до регістру
        string = string.lower()
        # обробляємо запит розбиваючи на команду та "все інше"
        if command := parse_command(string):
            command, args = command

            result = COMMANDS[command](*args)
            # перевірка результату на виключення
            if not isinstance(result, Exception):
                print(result)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
