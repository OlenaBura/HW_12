from collections import UserDict
from datetime import datetime
import pickle
import re
import sys
import time


class Field:
    def __init__(self):
        self.__value = None


class Name(Field):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class PhoneError(Exception):
    """Phone number must consist only from numbers and have format: +380XXXXXXXXX, +380-XX-XXX-XX-XX or without '+38'"""
    pass


class BirthdayError(Exception):
    """Birthday must have format 'DD.MM.YYYY' and consist only from numbers"""
    pass


class Phone(Field):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.search(r'^\+?3?8?(0[\s\-]?\d{2}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2})$', value):
            self.__value = value
        else:
            raise PhoneError("Phone number must consist only from numbers and have format: +380XXXXXXXXX, +380-XX-XXX-XX-XX or without '+38'")


class Birthday(Field):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if re.search(r'\d{2}\.\d{2}\.\d{4}', value):
            self.__value = value
        else:
            raise BirthdayError("Birthday must have format 'DD.MM.YYYY' and consist only from numbers")

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def __repr__(self) -> str:
        return f'Name: {self.name}, Phones: {self.phones}, Birthday: {self.birthday}'

    def add_phones(self, phone: Phone):
        if phone not in self.phones:
            self.phones.append(phone)

    def change_phones(self, phone, phone_new: Phone):
        for count, element in enumerate(self.phones):
            if element.value == phone:
                self.phones[count] = phone_new
                break

    def remove_phones(self, phone):
        for count, element in enumerate(self.phones):
            if element.value == phone:
                self.phones.remove(element)
                break

    def list_phones(self):
        return self.phones

    def add_birthday(self, birthday: Birthday):
        time.sleep(0.3)
        self.birthday = birthday

    def days_to_birthday(self, birthday):
        self.birthday = datetime.strptime(birthday.value, '%d.%m.%Y')
        now = datetime.now()
        delta1 = datetime(now.year, self.birthday.month, self.birthday.day)
        delta2 = datetime(now.year+1, self.birthday.month, self.birthday.day)
        return ((delta1 if delta1 > now else delta2) - now).days

    def sub_find_name_phone(self, value):
        if self.name.value.lower().find(value.lower()) != -1:
            time.sleep(0.3)
            print(self)
        else:
            for i in self.phones:
                if i.value.find(value) != -1:
                    time.sleep(0.3)
                    print(self)
                    break


class AddressBook(UserDict):
    def __repr__(self):
        return f'{self.data}'

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        return self.data

    def iterator(self, n=2):
        index = 0
        lst_temp = []
        for k, v in self.data.items():
            lst_temp.append(v)
            index = index + 1
            if index >= n:
                yield lst_temp
                lst_temp.clear()
                index = 0
        if lst_temp:
            yield lst_temp

    def show_all_limit(self, n=2):
        step = self.iterator(n)
        for i in range(len(self.data)):
            try:
                result = next(step)
                time.sleep(0.3)
                print(result)
                input("Press enter for next page:")
            except StopIteration:
                break

    def save_to_file(self, filename):
        with open(filename, 'wb') as fh:
            pickle.dump(self, fh)

    def read_from_file(self, filename):
        with open(filename, 'rb') as fh:
            self_unpack = pickle.load(fh)
            return self_unpack


def input_error_name_phone(func):
    def wrapper(lst, address_book):
        try:
            name, phone, *extra = lst
        except ValueError:
            time.sleep(0.3)
            print("Give me name and phone please. Format of phone must be +380XXXXXXXXX, +380-XX-XXX-XX-XX or without '+38'")
        else:
            return func(lst, address_book)
    return wrapper


def input_error_absent_contacts(func):
    def wrapper(lst, address_book):
        if len(address_book) == 0:
            try:
                next(filter(lambda d: d.get('name') == lst[0], address_book))
            except StopIteration:
                time.sleep(0.3)
                print("You haven't added any contact. Do it with command 'add'!")
            else:
                return func(lst, address_book)
        else:
            return func(lst, address_book)
    return wrapper


def input_error_name_birthday(func):
    def wrapper(lst, address_book):
        try:
            name, birthday, *extra = lst
        except ValueError:
            time.sleep(0.3)
            print("Give me name and birthday please. Birthday must have format 'DD.MM.YYYY' and consist only from numbers")
        else:
            return func(lst, address_book)
    return wrapper


def input_error_name_phone_phone_new(func):
    def wrapper(lst, address_book):
        try:
            name, phone, phone_new, *extra = lst
        except ValueError:
            time.sleep(0.3)
            print("Give me name, phone and new phone please. Format new phone must be +380XXXXXXXXX, +380-XX-XXX-XX-XX or without '+38'")
        else:
            return func(lst, address_book)
    return wrapper


def input_error_absent_name(func):
    def wrapper(lst, address_book):
        try:
            next(filter(lambda d: d.get('name') == lst[0], address_book))
        except StopIteration:
            time.sleep(0.3)
            print("The name is absent in AddressBook. If you want to save it, use the 'add' command")
        else:
            return func(lst, address_book)
    return wrapper


def input_error_number(func):
    def wrapper(lst, address_book):
        try:
            lst[1] = int(lst[1])
        except ValueError:
            time.sleep(0.3)
            print('Phone number must contain only digits! Try again, please')
        else:
            return func(lst, address_book)
    return wrapper


def input_error_filename(func):
    def wrapper(lst, address_book):
        try:
            filename = lst
        except ValueError:
            time.sleep(0.3)
            print("Give me filename please")
        else:
            return func(lst, address_book)
    return wrapper


def hello(lst, address_book: AddressBook):
    time.sleep(0.3)
    print("How can I help you?")


#@input_error_number
@input_error_name_phone
def add_name_phone(lst, address_book: AddressBook):
    name, phone, *extra = lst
    record = address_book.get(name)
    if record:
        record.add_phones(Phone(phone))
        time.sleep(0.3)
        print(address_book)
        time.sleep(0.3)
        print(f'New phone {phone} of {name} has just added')
    else:
        address_book.add_record(Record(Name(name), Phone(phone)))
        time.sleep(0.3)
        print(address_book)
        time.sleep(0.3)
        print(f'New contacts (name: {name}, phone: {phone}) has just added')


#@input_error_absent_name
@input_error_name_birthday
def add_name_birthday(lst, address_book: AddressBook):
    name, birthday, *extra = lst
    record = address_book.get(name)
    if record:
        record.add_birthday(Birthday(birthday))
        time.sleep(0.3)
        print(address_book)
        time.sleep(0.3)
        print(f'Birthday of {name} is added')


def find_name_phone(lst, address_book: AddressBook):
    value, *extra = lst
    for k, v in address_book.items():
        record = address_book.get(k)
        record.sub_find_name_phone(value)


@input_error_name_phone_phone_new
def change_phone(lst, address_book: AddressBook):
    name, phone, phone_new, *extra = lst
    record = address_book.get(name)
    if record:
        record.change_phones(phone, Phone(phone_new))
        time.sleep(0.3)
        print(address_book)
        time.sleep(0.3)
        print(f'Phone {phone} of {name} is changed. New phone is {phone_new}')


@input_error_name_phone
def remove_phone(lst, address_book: AddressBook):
    name, phone, *extra = lst
    record = address_book.get(name)
    if record:
        record.remove_phones(phone)
        time.sleep(0.3)
        print(address_book)
        time.sleep(0.3)
        print(f'Phone {phone} of {name} is removed')


@input_error_absent_contacts
def show_all(lst, address_book: AddressBook):
    if lst:
        n, *extra = lst
        address_book.show_all_limit(int(n))
    else:
        address_book.show_all_limit()


def bye_bot(lst, address_book: AddressBook):
    time.sleep(0.3)
    sys.exit('Good bye!')


@input_error_filename
def write_contacts_to_file(lst, address_book: AddressBook):
    filename, *extra = lst
    address_book.save_to_file(filename)
    print(f"AddressBook is saved to file '{filename}'")


@input_error_filename
def load_contacts_from_file(lst, address_book: AddressBook):
    filename, *extra = lst
    address_book.read_from_file(filename)


def main():
    address_book = AddressBook()

    while True:
        time.sleep(0.3)
        print('Enter your command, I know only 12 commands: hello, add, add birthday, change phone, remove phone, show all, find, save to, read from, good bye, close, exit:')
        command_entered = input('>>> ').lstrip()
        for i in COMMANDS.keys():
            if command_entered.lower().startswith(i):
                command = command_entered[:len(i)].lower()
                argument_lst = command_entered[len(i)+1:].lower().capitalize().split()
                COMMANDS[command](argument_lst, address_book)
                break


if __name__ == '__main__':

    COMMANDS = {'hello': hello, 'add birthday': add_name_birthday, 'add': add_name_phone,
                'change phone': change_phone, 'remove phone': remove_phone, 'find': find_name_phone,
                'save to': write_contacts_to_file, 'read from ': load_contacts_from_file,
                'show all': show_all, 'good bye': bye_bot, 'close': bye_bot, 'exit': bye_bot}
    main()