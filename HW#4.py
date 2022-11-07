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


def input_error(error_message):
    """ф-ція декоратор який вловлює похибки
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (KeyError, ValueError, IndexError, TypeError) as err:
                print(error_message)
                return err
        return inner
    return wrapper


@command("good_bye", "exit", "close")
@input_error("This command doesn't take arguments")
def goodbye():
    print("this is the end")
    exit()


@command("hello")
@input_error("This command doesn't take arguments")
def hello():
    return "How can I help you?"


@command(".")
@input_error("This command doesn't take arguments")
def nothing():
    exit()


@command('add')
@input_error("Enter name and number")
def add(name, number):
    """ф-ція запису в словник і інформації
    """
    CONTACTS[name] = number
    return ""


@command('show_all')
@input_error("This command doesn't take arguments")
def show_all():
    """ф-ція виводу записаної інформації
    """
    return CONTACTS


@command('phone')
@input_error("This command takes only Name arguments")
def phone(name):
    """ф-ція запиту значення словнику за ключем
    """
    return CONTACTS[name]


@command('change')
def change(name, number):
    """ф-ція команди "зміни". вносить зміну в значення словнику по ключу
    """
    CONTACTS[name] = number
    return ""


def main():
    """Головна ф-ція.
    Запускає нескінченний цикл, вихід з якого можно виконати за командами
    """
    while True:
        # запит на введеня інформації
        string = input("Command: ")
        # обробляємо запит розбиваючи на команду та "все інше"
        [command, *args] = string.split()
        # умова не чутливості до регістру
        command = command.lower()
        # перевірка на правильність вводу команди
        result = COMMANDS.get(
            command,
            lambda *_: "invalid command"
        )(*args)
        # перевірка результату на виключення
        if not isinstance(result, Exception):
            print(result)


if __name__ == "__main__":
    main()
