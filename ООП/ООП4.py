from abc import abstractmethod


class Info:
    @abstractmethod
    def info(self):
        pass


class Customer(Info):
    def __init__(self, name, email, customer_id):
        self._name = name
        self._email = email
        self._customer_id = customer_id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    @property
    def customer_id(self):
        return self._customer_id

    def info(self):
        return f'Your name is {self._name}\nYour email is {self._email}\nYour id is {self._customer_id}'

from random import randint

class BankAccount(Info):
    def __init__(self, balance, owner, account_number):
        self._balance = int(balance)
        self._owner = owner
        self._account_number = self.gen_acc_num()

    def gen_acc_num(self):
        return ''.join(str(randint(0, 5)) for _ in range(10))

    @property
    def balance(self):
        return self._balance

    def add_balance(self, num):
        if num > 0:
            self._balance += num
        else:
            print('Сума для внесення повинна бути більше нуля.')

    def minus_balance(self, num):
        if self._balance - num >= 0:
            self._balance -= num
        else:
            print('На вашому рахунку недостатньо коштів.')

    def return_bal(self):
        return f'Your balance is {self._balance}$!'

    @property
    def owner(self):
        return self._owner

    @property
    def account_number(self):
        return self._account_number

    def info(self):
        return f'Your balance is {self._balance}\nOwner is {self._owner}\nYour account number is {self._account_number}'

customer = Customer('Vadim', 'vadim01@gmail.com', 312553)
account = BankAccount(500, 'Vadim', 5)

print(customer.info())
print(account.info())
print(account.return_bal())

account.add_balance(100)
account.minus_balance(1000)
account.minus_balance(10)
print(account.return_bal())
print(account.account_number)
