import re

# if __name__ == "__main__":
#    main()


def add_contact():
    print("Enter Name and Number")
    contact = input("Enter Name and Number phone, format \"name xxx-xx-xx\"")
    name, number_phone = contact.split(" ")
    LIST_CONTACT[name] = number_phone
    return LIST_CONTACT


COMMANDS = {
    "hello": "How can I help you?",
    "add": add_contact(),
    "change": ["action2"],
    "phone": ["action3"],
    "show all": print(LIST_CONTACT),
    "good bye": ["Good bye"],
    "close": ["Good bye"],
    "exit": ["Good bye"],
}
LIST_CONTACT = {}

# нескінченний цикл запиту вводу інформації


def main():
    """Головна ф-ція. Нескінченний цикл вводу даних
    """
    while True:
        # ігнорування регістру
        string = input("")
        if string == '.':
            print("This is THE END")
            break
        else:
            enter_command = commands(string)
            print(enter_command)
            continue


def commands(com):
    """ф-ція карування команд"""
    return COMMANDS[com]


main()
