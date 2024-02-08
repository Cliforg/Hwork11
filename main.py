from collections import UserDict
from datetime import datetime

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value


    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and int(value):
            self.value = value
        else:
            raise ValueError('Number must hace 10 symbols')
        
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

    def __eq__(self, other):
        return isinstance(other, Phone) and self.value == other.value   


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d-%m-%Y')
            self.value = value
        except ValueError:
            print ('Date format must be DD-MM-YYYY')
        except AttributeError:
            print('Invalid value')

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value
          

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                self.phones.remove(ph)


    def edit_phone(self, old_phone, new_phone):
        check = False
        for ph in self.phones:
            if ph.value == old_phone:
                check = True
                try:
                    ph.value = new_phone
                except ValueError as e:
                    return e  
        if not check:
            raise ValueError('Number is not ixisting') 


    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone:
                return ph
            
    def days_to_birthday(self):
        if not self.birthday:
            raise ValueError('Birthday is not set')
        today = datetime.now().date()
        bday = datetime.strptime(f'{self.birthday.value[:5]}-{today.year}', '%d-%m-%Y').date()
        if bday < today:
            bday = datetime.strptime(f'{self.birthday.value[:5]}-{today.year+1}', '%d-%m-%Y').date()            
        return (bday - today).days
        
    def __repr__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: Record):
        if name in self.data:
            return self.data[name]

    def delete(self, name: Record):
        if name in self.data:
            del self.data[name]

    def iterator(self, value):
        counter = 0
        data_list = list(self.data.values())      
        while counter < len(self.data):
            yield data_list[counter: counter+value]
            counter += value
    
    
book = AddressBook()

john_record = Record('John', '10-10-1010')
john_record.add_phone('1234567812')

test_record = Record('Test')
test_record.add_phone('1111111111')

test1_record = Record('Test1')
test1_record.add_phone('2222222222')

test2_record = Record('Test2')
test2_record.add_phone('2222222222')

test3_record = Record('Test3')
test3_record.add_phone('5555555555')

book.add_record(john_record)
book.add_record(test_record)
book.add_record(test1_record)
book.add_record(test2_record)
book.add_record(test3_record)


iter = book.iterator(1)
for i in iter:
    print(i)