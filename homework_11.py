from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.is_valid_phone(value):
            raise ValueError("Invalid phone number format")
        self._value = value

    def is_valid_phone(self, value):
        phone_pattern = r'^\+\d{10}$'
        return re.match(phone_pattern, value) is not None

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(None)
        if value:
            self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.is_valid_birthday(value):
            raise ValueError("Invalid birthday date format")
        self._value = value

    def is_valid_birthday(self, value):
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        return re.match(date_pattern, value) is not None

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()
            next_birthday = datetime(today.year, birthday_date.month, birthday_date.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, birthday_date.month, birthday_date.day).date()
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

class AddressBook:
    def __init__(self):
        self.contacts = []

    def iterator(self, batch_size=10):
        index = 0
        while index < len(self.contacts):
            yield self.contacts[index:index + batch_size]
            index += batch_size

def main():

    phone1 = Phone("+6666666666")
    birthday1 = Birthday("1666-06-06")
    contact1 = Record("John Doe", phone1, birthday1)

    phone2 = Phone("invalid_number")
    birthday2 = Birthday("1999-09-09")
    contact2 = Record("Jane Smith", phone2, birthday2)

    book = AddressBook()
    book.contacts.append(contact1)
    book.contacts.append(contact2)

    for batch in book.iterator(batch_size=1):
        for contact in batch:
            print(f"Name: {contact.name}")
            print(f"Phone: {contact.phone.value}")
            if contact.birthday:
                print(f"Days to Birthday: {contact.days_to_birthday()}")

if __name__ == "__main__":
    main()