import pickle
from bot_entities import AddressBook


def save_data(book, filename="addressbook.pkl"):
    print("Saving data...")
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    print("Loading data...")
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено
