import uuid
import re

class Info:
    def info(self):
        pass

class Customer(Info):
    def __init__(self, name, email):
        self._name = name
        self._email = email
        self._customer_id = f'Your id is {uuid.uuid1()}'

    @property
    def name(self):
        try:
            if isinstance(self._name, str):
                return f'Your name is {self._name}.'
            else:
                return '!Oops... Error: <<Invalid name>>!'
        except Exception as e:
            return f'!Oops... Error: <<Invalid name>>!, {e}'
    @property
    def email(self):
        try:
            if re.match(r'\b\w+@gmail\.com\b', self._email):
            # if isinstance(self._email, str):
                return f'Your email is {self._email}.'
            else:
                return '!Oops... Error: <<Invalid email>>!'
        except Exception as e:
            return f'!Oops... Error: <<Invalid email>>!, {e}'

    def info(self):
        return f'Your name is {self.name}\nYour email is {self.email}\n{self._customer_id}'

class BankAccount(Info):
    def __init__(self, balance, owner):
        self._balance = int(balance)
        self._owner = owner
        self._account_number = f'Your account number is {uuid.uuid4()}'

    @property
    def balance(self):
        return f'Your balance is {self._balance}$!'

    def add_balance(self, num):
        if num > 0:
            self._balance += num
        else:
            print('Сума для внесення повинна бути більше нуля.')

    def withdraw_balance(self, num):
        if self._balance - num >= 0:
            self._balance -= num
        else:
            print('На вашому рахунку недостатньо коштів.')

    @property
    def owner(self):
        try:
            if re.match(r'^[a-zA-Z]+$', self._owner):
                return f'Owner is {self._owner}.'
            else:
                return '!Oops... Error: <<Invalid name>>!'
        except Exception as e:
            return f'!Oops... Error: <<Invalid name>>!, {e}'

    def info(self):
        return f'Your balance is {self._balance}\nOwner is {self.owner}\n{self._account_number}'

customer = Customer('Vadim', 'vadim01@gmail.com')
account = BankAccount(500, 'Vadim')

print(customer.info())
print(customer.email)
print(customer.name)
print(customer._customer_id)

print(account.info())
print(account.owner)
print(account._account_number)

account.add_balance(100)
account.withdraw_balance(1000)
account.withdraw_balance(10)
print(account.balance)
