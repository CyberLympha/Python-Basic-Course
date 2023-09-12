from abc import ABC, abstractmethod

class Person:
    '''Базовый класс для работы с сотрудниками как с людьми'''

    def __new__(cls, *args, **kwargs) -> None:
        """ 
        При создании объекта класса должен проверяться возраст 
        объекта, если возраст не проходит - класс не создается
        (создание класса происходит только тогда, когда __new__
        возвращает ссылку на объект класса)
        """

        age = kwargs.get('age', None)

        if age is not None and not 0 < age <= 100:
            print('Укажите корректный возраст, объект не создан')
            return

        instance = super().__new__(cls)
        return instance

    def __init__(self, name: str, surname:str, age: int) -> None:
        """
        инициализатор класса.
        __атрибут - приватный атрибут
        _атрибут - защищенный атрибут
        атрибут - публичный атрибут
        """
        self.__name = name
        self.__surname = surname
        self.__age = age

    # ниже прописаны сеттеры и геттеры для атрибутов класса,
    # которые позволяют управлять доступом для них.

    @property
    def name(self):
        return self.__name

    @property
    def surname(self):
        return self.__surname

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if 0 < value <= 100:
            self.__age = value

    def __str__(self):
        """
        Магический метод для реализации функции str()
        применительно к классу
        """
        return f"{self.name} {self.surname}"

    def __setattr__(self, name: str, value: any) -> None:
        """
        Магический метод, который вызывается при каждом изменении
        любого атрибута. Здесь нужен для проверки соответствия  
        возраста нужному диапазону.
        """
        if name == f"_{type(self).__name__}__age":
            if not (type(value) == int and 0 <= value <= 100):
                print('Некорректное значение возраста')
                return
        # метод должен возвращать оригинальный метод, иначе присвоение
        # работать не будет
        return object.__setattr__(self, name, value)


class Employee(Person, ABC):
    AGE_LIMITS = 49
    class_instances = [] # список для сохранения в нем объектов класса

    def __new__(cls, *args, **kwargs):
        """
        При создании объекта класса мы добавляем этот объект в список
        class instances, но здесь не реализовано удаление объекта из
        списка при удалении самого объекта (__del__).
        """
        # т.к. мы переопределяем метод __new__, то проверка возвраста
        # в классе-родителе производиться не будет, поэтому мы вручную
        # вызываем родительский метод __new__ с агрументом age
        instance = super().__new__(cls, age=args[3]) 
        cls.class_instances.append(instance)

        return instance

    def __init__(
            self,
            name,
            surname,
            position,
            age,
            currency='rub',
            salary=50_000):

        super().__init__(name, surname, age)

        self.__position = position
        self.__currency = currency
        self.__salary = salary
        self._verify_age(self.age)

    def __setattr__(self, name: str, value: any) -> None:

        if name == f"_{type(self).__name__}__salary":
            if not (type(value) in [int, float] and 0 <= value <= 100000):
                print('Некорректное значение зарплаты')
                return

        return object.__setattr__(self, name, value)

    def __call__(self):
        """
        Магический метод, который определяет поведение класса при
        обращении к нему как к функции, через ()
        """
        print(f"Сотрудник {self.__name} уже бежит к вам")

    def __eq__(self, other):
        """
        Определяет поведение класса при сравнении его с другим
        объектом через операцию ==
        """
        return self.name == other.name and self.surname == other.surname

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value):
        self.__currency = value

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        self.__salary = value

    @abstractmethod
    def give_premium(self):
        """
        Абстрактный метод добавлен, чтобы в дочерних классах
        этот метод был реализован в обязательном порядке
        """
        pass

    def change_currency(self, currency_new):
        if self.currency != currency_new:
            try:
                # обработчик мы написали, чтобы отлавливать
                # случаи, в которых у нас нет данных о курсе
                # валюты, в которую мы переводим
                self.salary = self.convert_currency(
                    self.salary,
                    self.currency,
                    currency_new
                )
                self.__currency = currency_new

            except KeyError:
                print('Недопустимое имя валют(ы)')

    @classmethod
    def _verify_age(cls, age):
        """
        Это метод класса, т.к. нам нужен доступ к атрибуту класса AGE_LIMITS
        """
        res = age <= cls.AGE_LIMITS

        if not res:
            print("Возраст сотрудника не удовлетворяет корп.стандартам")

        return res

    @staticmethod
    def convert_currency(value,
                         cur_currency,
                         req_currency):
        
        """_
        А это статический метод, у него нет доступа к атрибутам объекта и 
        класса, зато он может работать как калькулятор валют
        """

        exchange_rate = {
            'rub': 1,
            'usd': 90,
            'eur': 100
        }

        # Пересчет курса валют
        rate = (exchange_rate[cur_currency] /
                exchange_rate[req_currency])
        
        # Пересчет зарплаты
        result = value * rate

        return result


class Engineer(Employee):
    AGE_LIMITS = 50

    def __init__(self, *args, **kwargs):
        # Мы никак не меняем аргументы при инициализации,
        # но нам нужно создать атрибут manager, поэтому нам
        # нужен инициализатор, поэтому мы должны добавить 
        # вызов вышестоящего инициализатора с пробросом
        # всех параметров
        super().__init__(*args, **kwargs)
        self.manager = None # Ссылка на управляющего менеджера

    def give_premium(self):
        return self.salary * 0.1


class Manager(Employee):

    def __init__(self, name, surname, position, age, currency='rub', salary=60000):
        # а здесь мы явно указываем все параметры, т.к. мы меняем salary
        super().__init__(name, surname, position, age, currency, salary)
        self.engineers = list() # список для хранения списка инженеров

    def add_engineer(self, engineer):
        if engineer not in self.engineers:
            self.engineers.append(engineer)
            engineer.manager = self

    def give_premium(self):
        return sum([engineer.salary for engineer in self.engineers]) * 0.15

    def change_salary(self, new_salary, currency=None):
        old_salary = self.salary
        self.salary = new_salary

        if currency is not None and currency != self.currency:
            old_salary = self.convert_currency(
                old_salary, self.currency, currency)
            self.currency = currency

        if (new_salary - old_salary) / old_salary > 0.5:
            print("Подозрение на коррупционные схемы!")
