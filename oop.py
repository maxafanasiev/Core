from collections import UserDict
import datetime as DT
import pickle
import os


class AddressBook(UserDict):
    def addRecord(self,record):
        if record.name.value not in self.keys():
            self.data[record.name.value] = record
        else:
            print("Name already exist. Try add phone command for add extra phone.")


    def iterator(self, n=10):
        self.page = 0
        self.record_per_page = int(n)
        self.out = list(self.data.items())

        while True:
            start = self.page * self.record_per_page
            end = start + self.record_per_page
            page_record = self.out[start:end]

            if not page_record:
                return 

            self.page += 1

            yield page_record


    def __str__(self):
        page_num = 1
        out = '-'*100 + '\n'
        if self.keys():
            for page in self.iterator(5):
                out += '-'*100 + '\n'
                out += ' {:^98} \n'.format(f"Page #{page_num}")
                out += '-'*100 + '\n'
                out += '| {:^20} | {:^50} | {:^20} |\n'.format('Name', 'Phones', 'Birthday date')
                out += '-'*100 + '\n'
                for record in page:
                    out += str(record[1])
                page_num += 1
        else:
            out += '| {:^96} |\n'.format('Adress book is empty.')
        out += '-'*100 + '\n'
        return out


    def find(self, string:str):
        output = ''
        for key in self.keys():
            rec = self[key]
            phones = '.'.join(phone.value for phone in rec.phones)
            if string in str(rec.name.value) or string in phones:
                output += str(rec)
        return output
    
    
    def save_to_file(self, filename):
        with open(filename, mode="wb") as file:
            pickle.dump(self.data, file)
            print("Address book saved.")


    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as f:
                if os.stat(filename).st_size == 0:
                    self.data = {}
                else:
                    self.data = pickle.load(f)
                    print("Address book loaded.")
        except (FileNotFoundError, pickle.UnpicklingError):
            with open(filename, 'wb') as f:
                self.data = {}
                pickle.dump(self.data, f)


class Field:
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value
       
    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value:
            try:
                self._value = DT.datetime.strptime(value, '%d-%m-%Y')
            except ValueError:
                print('Print date in format dd-mm-YYYY')
                raise ValueError
        else:
            self._value = ''

    

class Phone(Field):  
    @property
    def value(self):
        return self._value


    @value.setter
    def value(self, value):
        if not value.isdigit() and value:
            print('Phone must be a numbers.')
            raise ValueError
        self._value = value


class Record:
    def __init__(self,name, phone=None, birthday=None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    
    def __str__(self):
        if self.phones:
            phones = ', '.join(phone.value for phone in self.phones)
        else:
            phones = 'No phones found.'
        bd = str(self.birthday.value.date()) if self.birthday.value else 'No birthday date.'
        return ('| {:<20} | {:^50} | {:^20} |\n'.format(self.name.value, phones, bd))


    def days_to_birthday(self):
        if self.birthday.value:
            bd = self.birthday.value
            if DT.datetime(DT.datetime.now().year,bd.month,bd.day) > DT.datetime.now():
                new_dt = DT.datetime(DT.datetime.now().year,bd.month,bd.day)
            else:
                new_dt = DT.datetime(DT.datetime.now().year + 1 ,bd.month,bd.day)
            res = new_dt - DT.datetime.now()
            return f"{res.days} days to {self.name.value} birthday!"
        else:
            return 'No found birthday date.'


    def add_phone(self, phone: Phone):
        if phone.value not in [phone.value for phone in self.phones]:
            self.phones.append(phone)
        else:
            print("This phone already added.")


    def add_birthday(self, birthday: Birthday):
        if birthday.value != self.birthday.value and not self.birthday.value:
            self.birthday = birthday
        else:
            print(f"{self.name.value} birthday already added.")


    def del_phone(self, phone: Phone):
        for n in self.phones:
            if n.value == phone.value:
                self.phones.remove(n)


    def change_phone(self,old_phone: Phone, new_phone: Phone):
        if old_phone.value == new_phone.value or new_phone.value in [phone.value for phone in self.phones]:
            print("This phone alredy exist!")
        elif old_phone.value not in [phone.value for phone in self.phones]:
            print("This phone not found!")
        else:
            for phone in self.phones:
                if old_phone.value == phone.value:
                    phone.value = new_phone.value
            print("Phone changed.")
