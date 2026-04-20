from helpers.decorate import line
from helpers.try_catch import try_catch
from colorama import Fore

# 1) Створіть дескриптор PositiveValue, який:
#    Дозволяє встановлювати лише додатні числа. 

class PositiveValue:
    '''
    Створіть дескриптор PositiveValue, який:
   Дозволяє встановлювати лише додатні числа. 
    '''
    def __get__(self, instance, owner):
        return instance.__balance

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("Balance must be a positive and not null.")
        instance.__balance = value

# Додайте ще один дескриптор Name для перевірки імені власника:
# - Ім’я має бути рядком.
# - Ім’я має містити лише літери та починатися з великої.
class Name:
    def __get__(self, instance, owner):
        return instance.__owner

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("Owner name must be a string.")
        if not value.isalpha():
            raise ValueError("Owner name must contain only letters.")
        
        normalized_value = value.strip()

        if not value[0].isupper():
            normalized_value = value[0].upper() + value[1:]
        
        if not value[1:].islower():
            normalized_value = normalized_value[0] + normalized_value[1:].lower()
                   

        instance.__owner = normalized_value


# Використайте цей дескриптор у класі BankAccount для перевірки балансу рахунку.
#    Додайте можливість створити об’єкт BankAccount із заданим ім’ям власника та початковими коштами.
#    Якщо спробувати встановити від’ємне значення або нуль — викидається ValueError.

class BankAccount:
    ''' 
    Використайте цей дескриптор у класі BankAccount для перевірки балансу рахунку.
    Додайте можливість створити об’єкт BankAccount із заданим ім’ям власника та початковими коштами.
    Якщо спробувати встановити від’ємне значення або нуль — викидається ValueError.
    
    '''
    balance = PositiveValue()
    owner = Name()
    def __init__(self, owner: str, initial_balance: float):
        self.owner = owner
        self.balance = initial_balance




# 2) Створіть дескриптор LogDescriptor, який:
#    Логує кожен доступ до атрибута, включаючи читання та запис.

class LogDescriptor:
    '''
    Створіть дескриптор LogDescriptor, який:
    Логує кожен доступ до атрибута, включаючи читання та запис.
    '''
    def __get__(self, instance, owner):
        print (f"{Fore.LIGHTBLACK_EX}[LOG] Call")
        return instance.__field

    def __set__(self, instance, value):
        
        print (f"{Fore.LIGHTBLACK_EX}[LOG] Update")
        instance.__field = value

    def __delete__(self, instance):
        print (f"{Fore.LIGHTBLACK_EX}[LOG] Delete")
        del instance.__field



# 3) Напишіть метаклас, який не дозволяє створювати класи з атрибутами, що починаються з підкреслення.
#    Якщо клас містить такі атрибути, метаклас має викидати виняток.
#    Реалізуйте метаклас, який перевіряє атрибути класу на відповідність цьому обмеженню.
#    Напишіть кілька класів з атрибутами, що починаються з підкреслення, і переконайтеся, що буде викинуто виняток.

class NoUnderscore(type):
    '''
    3) Напишіть метаклас, який не дозволяє створювати класи з атрибутами, що починаються з підкреслення.
   Якщо клас містить такі атрибути, метаклас має викидати виняток.
   Реалізуйте метаклас, який перевіряє атрибути класу на відповідність цьому обмеженню.
   Напишіть кілька класів з атрибутами, що починаються з підкреслення, і переконайтеся, що буде викинуто виняток.
    '''
    def __new__(cls, name, bases, attrs):
        for attr in attrs:
            if (attr.startswith("__") and attr.endswith("__")):
                continue
            if attr.startswith("_"):                
                raise SyntaxError(f"[ERROR] Class {name} cannot have attributes that start with an underscore.")
            print (f"{Fore.LIGHTBLACK_EX}[LOG] Checking attribute: {attr} successfully.")

        print (f"{Fore.LIGHTBLACK_EX}[LOG] Class {name} created successfully.")
        return super().__new__(cls, name, bases, attrs)



# 4) Створіть метаклас, який автоматично додає в кожен клас метод hello(), який виводить рядок "Hello from <ім’я класу>".
#    Реалізуйте метаклас, який додає метод hello() в кожен клас.
#    Напишіть кілька класів, що використовують цей метаклас, і викличте метод hello() для кожного класу.

class AddHello(type):
    '''
    4) Створіть метаклас, який автоматично додає в кожен клас метод hello(), який виводить рядок "Hello from <ім’я класу>".
   Реалізуйте метаклас, який додає метод hello() в кожен клас.
   Напишіть кілька класів, що використовують цей метаклас, і викличте метод hello() для кожного класу.
    '''
    def __new__(cls, name, bases, attrs):
        def hello(self):
            print (f"Hello from {name}!")
        attrs["hello"] = hello
        return super().__new__(cls, name, bases, attrs)


# 5) Напишіть метаклас, який не дозволяє класам наслідувати інші класи, якщо в імені батьківського класу є підрядок "Forbidden".
#    Реалізуйте метаклас, який перевіряє ім’я батьківського класу та забороняє наслідування від класів із підрядком "Forbidden" в імені.
#    Напишіть кілька класів із цим метакласом і спробуйте створити клас, що наслідується від забороненого класу.

class DontUseForbidden(type):
    '''
    5) Напишіть метаклас, який не дозволяє класам наслідувати інші класи, якщо в імені батьківського класу є підрядок "Forbidden".
   Реалізуйте метаклас, який перевіряє ім’я батьківського класу та забороняє наслідування від класів із підрядком "Forbidden" в імені.
   Напишіть кілька класів із цим метакласом і спробуйте створити клас, що наслідується від забороненого класу.

    '''
    def __new__(cls, name, bases, attrs):
        for base in bases:
            if "Forbidden" in base.__name__:
                raise SyntaxError(f"[ERROR] Class {name} cannot inherit from class {base.__name__} because it contains 'Forbidden' in its name.")
        return super().__new__(cls, name, bases, attrs)


# 6) Створіть метаклас, який перевіряє, що кожен атрибут класу є рядком. Якщо атрибут не є рядком — викидайте виняток.
#    Реалізуйте метаклас, який перевіряє тип атрибутів класу.
#    Напишіть клас із атрибутами різних типів (наприклад, рядками та числами) і переконайтеся, що метаклас викидає виняток, якщо тип атрибута некоректний.

class UseOnlyStrings(type):
    '''
    6) Створіть метаклас, який перевіряє, що кожен атрибут класу є рядком. Якщо атрибут не є рядком — викидайте виняток.
   Реалізуйте метаклас, який перевіряє тип атрибутів класу.
   Напишіть клас із атрибутами різних типів (наприклад, рядками та числами) і переконайтеся, що метаклас викидає виняток, якщо тип атрибута некоректний.
    '''
    def __new__(cls, name, bases, attrs):
        for _name, value in attrs.items():
            if (_name.startswith("__") and _name.endswith("__")):
                continue
            if not isinstance(value, str):
                raise TypeError(f"[ERROR] Attribute {_name} in class {name} must be a string, but got {type(value).__name__}.")
            print (f"{Fore.LIGHTBLACK_EX}[LOG] Checking attribute: {_name} successfully.")
        print (f"{Fore.LIGHTBLACK_EX}[LOG] Class {name} created successfully.")
        return super().__new__(cls, name, bases, attrs)

# 7) Створіть протокол Shape, який вимагає реалізації методу area() для обчислення площі фігури. Реалізуйте кілька класів, таких як Circle, Rectangle і Triangle, які будуть реалізовувати цей протокол.
#    Напишіть функцію, яка приймає об’єкти, що реалізують протокол Shape, і виводить їх площу.
#    Протокол Shape має містити метод area().
#    Класи Circle, Rectangle і Triangle повинні реалізовувати метод area(), відповідний їхній геометричній формі.
#    Функція print_area() має приймати об’єкт, що реалізує протокол Shape, і виводити площу.
from typing import Protocol, List, runtime_checkable

@runtime_checkable
class Shape(Protocol):
    '''
    7) Створіть протокол Shape, який вимагає реалізації методу area() для обчислення площі фігури. 
    Реалізуйте кілька класів, таких як Circle, Rectangle і Triangle, які будуть реалізовувати цей протокол.

        - Напишіть функцію, яка приймає об’єкти, що реалізують протокол Shape, і виводить їх площу.
        - Протокол Shape має містити метод area().
        - Класи Circle, Rectangle і Triangle повинні реалізовувати метод area(), відповідний їхній геометричній формі.
        - Функція print_area() має приймати об’єкт, що реалізує протокол Shape, і виводити площу.
    '''
    def area(self) -> float:
        '''calc for a area'''
        pass

class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14 * self.radius ** 2
    
class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height
    
class Triangle:
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height
    
@try_catch
def print_area_if_shape(collection: List[Shape]):
    for item in collection:
        if isinstance(item, Shape):
            print (f"Area: {item.area()}")
        else:
            print (f"{Fore.YELLOW}Warning: Object {item.__class__.__name__} does not implement the Shape protocol.")



# 8) Створіть протокол Serializable, який вимагає реалізації методу serialize(). Реалізуйте два класи: Person і Book, які будуть реалізовувати цей метод для перетворення об’єктів у рядковий формат JSON.
#    Протокол Serializable має містити метод serialize().
#    Класи Person і Book повинні реалізовувати метод serialize(), що повертає рядок у форматі JSON.
#    Напишіть функцію serialize_object(), яка прийматиме об’єкт і викликатиме його метод serialize().

@runtime_checkable
class Serializable(Protocol):
    '''
    8) Створіть протокол Serializable, який вимагає реалізації методу serialize(). 
    
    Реалізуйте два класи: Person і Book, які будуть реалізовувати цей метод для перетворення об’єктів у рядковий формат JSON.
   Протокол Serializable має містити метод serialize().

   Класи Person і Book повинні реалізовувати метод serialize(), що повертає рядок у форматі JSON.

   Напишіть функцію serialize_object(), яка прийматиме об’єкт і викликатиме його метод serialize().
    '''
    def serialize(self) -> str:
        '''serialize object to json'''
        pass

import json

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        
    def serialize(self) -> str:
        return json.dumps({"name": self.name, "age": self.age})
    
class Book:
    def __init__(self, title: str, author: Person):
        self.title = title
        self.author = author

    def serialize(self) -> str:
        return json.dumps({
            "title": self.title, 
            "author": json.loads(self.author.serialize())
        })


def serialize_object(obj: Serializable):
    if isinstance(obj, Serializable):
        return obj.serialize()
    else:
        raise TypeError(f"Object of type {obj.__class__.__name__} does not implement the Serializable protocol.")
    


'''
=====================Work area=============================

'''

@try_catch
def task1():
    '''
1) Створіть дескриптор PositiveValue, який:
   Дозволяє встановлювати лише додатні числа. Використайте цей дескриптор у класі BankAccount для перевірки балансу рахунку.
   Додайте можливість створити об’єкт BankAccount із заданим ім’ям власника та початковими коштами.
   Якщо спробувати встановити від’ємне значення або нуль — викидається ValueError.

Додайте ще один дескриптор Name для перевірки імені власника:
- Ім’я має бути рядком.
- Ім’я має містити лише літери та починатися з великої.

    '''
    line("Task 1", color= Fore.MAGENTA)
    account = BankAccount("Samantha", 1000)
    print (f"Owner: {account.owner}, Balance: {account.balance}")
  
    line("Name change")
    account.owner = "sAnS"
    print (f"Owner: {account.owner}, Balance: {account.balance}")


    line("Try to set invalid balance")
    account.balance = -500
    print (f"Owner: {account.owner}, Balance: {account.balance}")


def task2():
    '''2) Створіть дескриптор LogDescriptor, який:
    Логує кожен доступ до атрибута, включаючи читання та запис.
     '''
    line("Task 2", color= Fore.MAGENTA)
    class Sample:
        field = LogDescriptor()

        def __init__(self, field):
            self.field = field

    s = Sample("Hello")
    print (s.field)
    del s.field
    
@try_catch
def task3():
    '''
    3) Напишіть метаклас, який не дозволяє створювати класи з атрибутами, що починаються з підкреслення.
   Якщо клас містить такі атрибути, метаклас має викидати виняток.
   Реалізуйте метаклас, який перевіряє атрибути класу на відповідність цьому обмеженню.
   Напишіть кілька класів з атрибутами, що починаються з підкреслення, і переконайтеся, що буде викинуто виняток.
    '''
    line("Task 3", color= Fore.MAGENTA)
    
    class Sample(metaclass=NoUnderscore):
        field = "Hello"

    try:
        class ErrorSample(metaclass=NoUnderscore):
            _field = "Hello"
    except SyntaxError as e:
        print (f"{Fore.RED}Error: {e}")

    try:
        class ErrorSample2(metaclass=NoUnderscore):
            field = "field"
            __field = "Hello"
    except SyntaxError as e:
        print (f"{Fore.RED}Error: {e}")


@try_catch
def task4():
    '''
    4) Створіть метаклас, який автоматично додає в кожен клас метод hello(), який виводить рядок "Hello from <ім’я класу>".
   Реалізуйте метаклас, який додає метод hello() в кожен клас.
   Напишіть кілька класів, що використовують цей метаклас, і викличте метод hello() для кожного класу.
    '''
    line("Task 4", color= Fore.MAGENTA)
    class Sample(metaclass=AddHello):
        pass
    s = Sample()
    s.hello()
    
    OwnClass = AddHello("OwnClass", (), {
        "method": lambda self: print("I`m method i`m exists")
    })

    o = OwnClass()
    o.hello()
    o.method()
    
@try_catch
def task5():
    '''
    5) Напишіть метаклас, який не дозволяє класам наслідувати інші класи, якщо в імені батьківського класу є підрядок "Forbidden".
   Реалізуйте метаклас, який перевіряє ім’я батьківського класу та забороняє наслідування від класів із підрядком "Forbidden" в імені.
   Напишіть кілька класів із цим метакласом і спробуйте створити клас, що наслідується від забороненого класу.

    '''
    line("Task 5", color= Fore.MAGENTA)
    class ForbiddenBase:
        pass

    class NormalBase:
        pass

    class Sample(metaclass=DontUseForbidden):
        pass

    class ChildSample(NormalBase, metaclass=DontUseForbidden):
        pass

    class IWillFail(ForbiddenBase, metaclass=DontUseForbidden):
        pass

@try_catch
def task6():
    '''
    
    6) Створіть метаклас, який перевіряє, що кожен атрибут класу є рядком. Якщо атрибут не є рядком — викидайте виняток.
   Реалізуйте метаклас, який перевіряє тип атрибутів класу.
   Напишіть клас із атрибутами різних типів (наприклад, рядками та числами) і переконайтеся, що метаклас викидає виняток, якщо тип атрибута некоректний.'''
    line("Task 6", color= Fore.MAGENTA)
    class Sample(metaclass=UseOnlyStrings):
        field1 = "Hello"
        field2 = "World"
        # field3 = 123
    
    class IWailFailAfterField1(metaclass=UseOnlyStrings):
        field1 = "Hello"
        field2 = 123


@try_catch
def task7():
    '''
    7) Створіть протокол Shape, який вимагає реалізації методу area() для обчислення площі фігури. Реалізуйте кілька класів, таких як Circle, Rectangle і Triangle, які будуть реалізовувати цей протокол.

        - Напишіть функцію, яка приймає об’єкти, що реалізують протокол Shape, і виводить їх площу.
        - Протокол Shape має містити метод area().
        - Класи Circle, Rectangle і Triangle повинні реалізовувати метод area(), відповідний їхній геометричній формі.
        - Функція print_area() має приймати об’єкт, що реалізує протокол Shape, і виводити площу.
        '''
    
    line("Task 7", color= Fore.MAGENTA)
    circle = Circle(5)
    rectangle = Rectangle(2, 5)
    triangle = Triangle(1, 3)

    class Banana:
        pass
        
    banana = Banana()

    class Sample:
        pass

    s = Sample()
    print_area_if_shape([circle, rectangle, triangle, s, banana])
    

@try_catch
def task8():
    '''
    8) Створіть протокол Serializable, який вимагає реалізації методу serialize(). Реалізуйте два класи: Person і Book, які будуть реалізовувати цей метод для перетворення об’єктів у рядковий формат JSON.
    Протокол Serializable має містити метод serialize().
    Класи Person і Book повинні реалізовувати метод serialize(), що повертає рядок у форматі JSON.
    Напишіть функцію serialize_object(), яка прийматиме об’єкт і викликатиме його метод serialize().
    '''
    line("Task 8", color= Fore.MAGENTA)
    person = Person("Alice", 30)
    book = Book("Book", person)

    print (serialize_object(person))
    print (serialize_object(book))


if __name__ == "__main__":
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()