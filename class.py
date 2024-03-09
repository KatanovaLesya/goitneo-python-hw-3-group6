from collections import UserDict, defaultdict
from datetime import datetime, timedelta

#Базовий клас для полів запису
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

#Клас для зберігання імені контакту. 
class Name(Field):
    def __init__(self, value: str):
        if not value.isalpha():
            print("The name must consist letters only")
            raise ValueError
        if not value.istitle():
            print("The name must start with an upper case letter and the rest letter must be lower case")
            raise ValueError
        self.value = value

#Клас для зберігання дати народження.
class Birthday:
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except:
            print("The birthday date must be in format DD.MM.YYYY")
            raise ValueError
        self.value = value
   

#Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    def __init__(self, value: str):
        if not all([len(value) == 10, value.isdigit()]):
            print("The phone number must consist of 10 digits")
            raise ValueError
        self.value = value


#Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

#Додавання телефонів.Видалення телефонів.Редагування телефонів.Пошук телефону.    
    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if str(self.phones[i]) == old_phone:
                self.phones[i] = Phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
    
    def add_birthday(self, birthday):
        birthday = Birthday(birthday)
        self.birthday = birthday
        return(self.birthday)
                        
    def show_birthday(self):
        birthday = str(self.birthday.value)
        return (birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

#Клас для зберігання та управління записами.
class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, value):
        if not (self.data.get(value)):
            print("There is not such name in AddressBook")
            raise ValueError
        return(self.data.get(value))

    def delete(self, name):
        del self.data[name]

    def week_birthdays(self,contacts):
        list_of_birthday = defaultdict(list)
        today = datetime.today().date()
        tomorrow = today + timedelta(days=1)
        for name, record in contacts.data.items():
            rec = contacts.find(name)
            birthday = datetime.strptime(rec.show_birthday(), '%d.%m.%Y')
            birthday_this_year = birthday.replace(year=tomorrow.year)
            birthday_this_year = datetime.date(birthday_this_year)
            if birthday_this_year < tomorrow:
                birthday_this_year = birthday_this_year.replace(year = (tomorrow.year + 1))
            delta_days = (birthday_this_year - tomorrow).days
            if delta_days < 7:
                day_of_week = birthday_this_year.weekday()
                if day_of_week == 0:
                    list_of_birthday["Monday"].append(name)
                elif day_of_week == 1:
                    list_of_birthday["Tusday"].append(name)
                elif day_of_week == 2:
                    list_of_birthday["Wenesday"].append(name)
                elif day_of_week == 3:
                    list_of_birthday["Thursday"].append(name)
                elif day_of_week == 4:
                    list_of_birthday["Friday"].append(name)
                elif day_of_week == 5 and today.weekday() != 5 and today.weekday() != 6:
                    list_of_birthday["Monday"].append(name)
                elif day_of_week == 6 and today.weekday() != 6:
                    list_of_birthday["Monday"].append(name)
        return(list_of_birthday)
