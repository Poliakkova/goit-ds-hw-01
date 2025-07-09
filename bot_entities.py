from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone:str):
        if len(phone) != 10 or not phone.isdigit():
            raise ValueError("Wrong phone format. Must be 10 digits")
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


    def show_birthday(self):
        return self.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_phone(self, phone: str, index:int = -1):
        phone_item = Phone(phone)
        existing_phone = self.find_phone(phone)

        if existing_phone is not None:
            raise ValueError('Duplicate phone numbers. Not added')

        if index < 0:
            self.phones.append(phone_item)
        else:
            self.phones.insert(index, phone_item)


    def remove_phone(self, phone: str):
        phone_item = self.find_phone(phone)
        self.phones.remove(phone_item)


    def edit_phone(self, old_phone: str, new_phone: str):
        old_phone_item = self.find_phone(old_phone)
        if old_phone_item is None:
            raise ValueError("Given old phone number not found")

        phone_index = self.phones.index(old_phone_item)
        self.add_phone(new_phone, phone_index)
        self.remove_phone(old_phone)


    def find_phone(self, phone: str):
        phone_item = list(filter(lambda item: item.value == phone, self.phones))
        if len(phone_item) == 0:
            return None
        return phone_item[0]


    def add_birthday(self, value: str):
        birthday = Birthday(value)
        self.birthday = birthday


    def show_birthday(self):
        return self.birthday.show_birthday() if self.birthday else 'None'

    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(p.value for p in self.phones)}, "
                f"birthday: {self.show_birthday()}")


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find (self, name: str):
        return self.data.get(name)

    def delete (self, name: str):
        self.data.pop(name)

    def get_upcoming_birthdays(self, days = 7):
        upcoming_birthdays = []
        today = date.today()

        for record in self.data.values():
            if record.birthday:
                datetime_object = datetime.strptime(record.birthday.value, "%d.%m.%Y")
                birthday_this_year = datetime_object.replace(year=today.year).date()

                # якщо вже було цього року
                if birthday_this_year < today:
                    birthday_this_year = datetime_object.replace(year=today.year + 1).date()

                if 0 <= (birthday_this_year - today).days <= days:
                    # перенести на понеділок, якщо вихідний
                    birthday_this_year = self.__adjust_for_weekend(birthday_this_year)

                    congratulation_date_str = self.__date_to_string(birthday_this_year)
                    upcoming_birthdays.append({"name": record.name.value, "congratulation_date": congratulation_date_str})
        return upcoming_birthdays

    def __adjust_for_weekend(self, birthday):
        if birthday.weekday() >= 5:
            return self.__find_next_weekday(birthday, 0)
        return birthday

    def __find_next_weekday(self, start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    def __date_to_string(self, date):
        return date.strftime("%Y.%m.%d")

    def __str__(self):
        if not self.data:
            return "AddressBook:\nNo records\n"
        return f"AddressBook ({len(self.data)} records):\n" + "\n".join(str(record) for record in self.data.values()) + "\n"


if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1111111111")
    john_record.add_phone("3333333333")
    john_record.add_phone("5555555555")
    try:
        john_record.add_phone("000")
    except ValueError as e:
        print('ValueError! -', e) # ValueError! - Wrong format

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    try:
        jane_record.add_phone("9876543210")
    except ValueError as e:
        print('ValueError! -', e) # ValueError! - Duplicate

    book.add_record(jane_record)
    print()

    # Виведення всіх записів у книзі
    print(book)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("3333333333", "1112223333")
    try:
        john.edit_phone("2222222222", "2020202020")
    except ValueError as e:
        print('ValueError! -', e) # ValueError! - Item not found

    try:
        john.edit_phone("1112223333", "20")
    except ValueError as e:
        print('ValueError! -', e) # ValueError! - Wrong format

    print(john, '\n') # Contact name: John, phones: 1111111111; 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555
    found_phone = john.find_phone("000")
    print(f"{john.name}: {found_phone}\n")  # Виведення: John: None

    # Видалення запису Jane
    book.delete("Jane")

    # Виведення всіх записів у книзі
    print(book)