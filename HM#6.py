from collections import UserDict

COMMANDS = {}  # словник команд


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


CONTACTS = AddressBook()  # словник контактів


class Field:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"<Field value={self.value}>"

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        else:
            raise TypeError("Field can only be compared to Field")

    def __lt__(self, other):
        if isinstance(other, Field):
            return self.value < other.value
        else:
            raise TypeError("Field can only be compared to Field")

    def __le__(self, other):
        if isinstance(other, Field):
            return self.value <= other.value
        else:
            raise TypeError("Field can only be compared to Field")

    def __ne__(self, other):
        if isinstance(other, Field):
            return self.value != other.value
        else:
            raise TypeError("Field can only be compared to Field")

    def __gt__(self, other):
        if isinstance(other, Field):
            return self.value > other.value
        else:
            raise TypeError("Field can only be compared to Field")

    def __ge__(self, other):
        if isinstance(other, Field):
            return self.value >= other.value
        else:
            raise TypeError("Field can only be compared to Field")


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:
    def __init__(self, name, phone=None):
        self.name = name
        if phone:
            self.phone = phone
        else:
            self.phone = []

    def __repr__(self):
        return f"<Record name={self.name} phone={self.phone}>"

    def add_phone(self, phone):
        self.phone.append(phone)

    def remove_phone(self, phone):
        self.phone = list(
            filter(lambda ins_phone: ins_phone != phone, self.phone))

    def change_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)


def command(*args):
    """ф-ція декоратор команд.
    на вхід приймає аргумент яку сприймаємо як ф-цію
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        for x in args:
            COMMANDS[x.lower()] = inner
        return inner
    return wrapper


def input_error(error_message_dict):
    """ф-ція декоратор який вловлює похибки
    """
    def wrapper(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as err:
                if err.__class__ in error_message_dict.keys():
                    print(error_message_dict[err.__class__])
                    return err
                raise err
        return inner
    return wrapper


@command("good bye", "exit", "close")
@input_error({TypeError: "This command doesn't take arguments"})
def goodbye():
    print("this is the end")
    exit()


@command("hello")
@input_error({TypeError: "This command doesn't take arguments"})
def hello():
    return "How can I help you?"


@command(".")
@input_error({TypeError: "This command doesn't take arguments"})
def nothing():
    exit()


@command('add')
@input_error({TypeError: "Enter name and number"})
def add(name, number):
    """ф-ція запису в словник інформації
    """

    if name in CONTACTS.data.keys():
        CONTACTS.data[name].add_phone(Phone(number))
    else:
        record = Record(
            name=Name(name),
            phone=[Phone(number)]
        )
        CONTACTS.add_record(record)
    return ""


@command('show all')
@input_error({TypeError: "This command doesn't take arguments"})
def show_all():
    """ф-ція виводу записаної інформації
    """
    return CONTACTS.data


@command('phone')
@input_error({TypeError: "This command takes only Name arguments"})
def phone(name):
    """ф-ція запиту значення словнику за ключем
    """
    return CONTACTS.data[name].phone


@command('change')
@input_error({
    KeyError: "Non-existing name",
    TypeError: "This command takes Name, old phone and new_phone arguments"
})
def change(name, old_number, new_number):
    """ф-ція команди "зміни". вносить зміну в значення словнику по ключу
    """
    record = CONTACTS[name]
    record.change_phone(Phone(old_number), Phone(new_number))
    return ""


def parse_command(string: str):
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
