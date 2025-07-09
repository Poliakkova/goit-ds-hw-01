"""
Доробіть консольного бота помічника з попереднього домашнього завдання
"""
import colorama
from bot_entities import AddressBook, Record
from serialization import load_data, save_data

colorama.init(autoreset=True)


def input_error(func):
    """
    Decorator to process errors
    :param func: Callable
    :return: Callable
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except (ValueError, KeyError) as e:
            return colorama.Fore.RED + f"🔴 Error! {e.args[0]}"

        except IndexError as e:
            return colorama.Fore.RED + "🔴 Error! Wrong arguments. Must be: [command] [name]"

    return inner


@input_error
def main():
    """
    Communicates with user, parses inputs
    """
    book = load_data()

    print(colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX +
          "Welcome to bot-assistant 📞Phone Book📞! What can I help you with? 😊")
    print(show_help())

    while True:
        input_str = input(">> ").strip()
        if input_str == '':
            continue

        command, *args = parse_input(input_str)

        if command in ('exit', 'close'):
            break
        if command == 'hello':
            print('How can I help you?')
        elif command == 'help':
            print(show_help())
        elif command == 'add':
            print(add_contact(args, book))
        elif command == 'change':
            print(change_contact(args, book))
        elif command == 'phone':
            print(find_contact(args, book))
        elif command == 'all':
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print(colorama.Fore.YELLOW +
                  "⚠️ It's not a command. Type 'help' to see available commands")

    save_data(book)
    print(colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX +
          "Good bye! 😊")


@input_error
def parse_input(input_str: str):
    """
    Breaks string into command and arguments
    :param input_str: str
    :return: str, list
    """
    command, *args = input_str.split()
    command = command.strip().lower()
    return command, *args


def show_help():
    """
    Returns formatted command list
    :return: str
    """
    return ("Command list:\n"
            "\tadd [name] [phone number]             | add new name and phone number\n"
            "\tphone [name]                          | find phone number by person's name\n"
            "\tchange [name] [old phone] [new phone] | edit old phone number by person's name\n"
            "\tall                                   | show all phone numbers\n"
            "\tadd-birthday [name] [birthday]        | add birthday to contact\n"
            "\tshow-birthday [name]                  | show birthday by name\n"
            "\tbirthdays                             | show upcoming birthdays\n"
            "\thelp                                  | if you need to see this commands again\n"
            "\texit / close                          | to close bot-assistant")


@input_error
def change_contact(args, book:AddressBook):
    """
    Changes existing contact
    :param args: list
    :param book: AddressBook
    :return: str
    """
    if len(args) < 3:
        raise ValueError("Wrong arguments. Must be: change [name] [old phone] [new phone]")

    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError(f"Contact with name '{name}' not found")

    if old_phone and new_phone:
        record.edit_phone(old_phone, new_phone)

    return colorama.Fore.GREEN + '✅ Contact changed!'


@input_error
def add_contact(args, book:AddressBook):
    """
    Adds new contact if not exists yet
    :param args: list
    :param book: AddressBook
    :return: str
    """
    if len(args) < 2:
        raise ValueError("Wrong arguments. Must be: add [name] [phone]")

    name, phone, *_ = args
    record = book.find(name)
    message = colorama.Fore.GREEN + "✅ Contact updated!"

    if record is None:
        record = Record(name)
        message = colorama.Fore.GREEN + '✅ New name! Contact added'

    if phone:
        record.add_phone(phone)
        book.add_record(record)
    return message


@input_error
def find_contact(name, book:AddressBook):
    """
    Returns contact if found
    :param name: list
    :param book: AddressBook
    :return: str
    """
    record = book.find(name[0])
    if record is None:
        raise KeyError(f"Contact with name '{name[0]}' not found")
    return record.__str__()


@input_error
def show_all(book:AddressBook):
    """
    Return a formatted string of contacts list
    :param book:AddressBook
    :return: str
    """
    return book.__str__()


@input_error
def add_birthday(args, book:AddressBook):
    """
    Add birthday to contact
    :param args:
    :param book: AddressBook
    """
    if len(args) < 2:
        raise ValueError("Wrong arguments. Must be: add-birthday [name] [birthday]")

    name, birthday, *_ = args
    record = book.find(name)
    message = colorama.Fore.GREEN + '✅ Contact updated!'

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = colorama.Fore.GREEN + '✅ New name! Contact added'

    if birthday:
        record.add_birthday(birthday)
    return message


@input_error
def show_birthday(name, book:AddressBook):
    """
    Displays birthday
    :param args:
    :param book: AddressBook
    """
    record = book.find(name[0])
    if record:
        return "Birthday: " + record.show_birthday()
    raise KeyError(f"Contact with name '{name[0]}' not found")


@input_error
def birthdays(args, book:AddressBook):
    """
    Shows upcoming birthdays in 7 days or given in arguments
    :param args:
    :param book: AddressBook
    """
    days = 7
    if len(args) > 0 and int(args[0]):
        days = int(args[0])
    birthdays = book.get_upcoming_birthdays(days)

    return (f"Upcoming birthdays for {days} days\n"
            "Date       | Name\n"
            f"{'\n'.join(birthday['congratulation_date']+' | '+birthday['name'] for birthday in birthdays)}\n")


if __name__ == '__main__':
    main()
