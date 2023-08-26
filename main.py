import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Phone(Field):
    def __init__(self, value):
        super().__init__(None)
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        if not re.match(r'^\d{9}$', new_value):
            raise ValueError("Phone number must have 9 digits")
        self._value = new_value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(None)
        self.value = value

    @Field.value.setter
    def value(self, new_value):
        if not isinstance(new_value, datetime):
            raise ValueError("Birthday value must be a datetime object")
        self._value = new_value

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = Phone(phone) if phone else None
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today()
            next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left

class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def __iter__(self):
        return self.iterator()

    def iterator(self, batch_size=10):
        for i in range(0, len(self.records), batch_size):
            yield self.records[i:i + batch_size]

# Приклад використання:
address_book = AddressBook()

record1 = Record("Oleg Babay", phone="123456789", birthday=datetime(1999, 5, 15))
record2 = Record("Olya Kozlova", phone="987654321")


address_book.add_record(record1)
address_book.add_record(record2)


for batch in address_book:
    for record in batch:
        print(f"Name: {record.name}")
        if record.phone:
            print(f"Phone: {record.phone.value}")
        if record.birthday:
            print(f"Days to Birthday: {record.days_to_birthday()} days")
        print("-----")
