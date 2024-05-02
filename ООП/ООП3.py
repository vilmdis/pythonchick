# class A:
#     def introduce(self):
#         print('class A')


# class B(A):
#     def introduce(self):
#         super().introduce()
#         print('class B')


# class C(A):
#     def introduce(self):
#         super().introduce()
#         print('class C')


# class D(B, C):
#     def introduce(self):
#         super().introduce()
#         print('class D')

# d = D()
# d.introduce()


class Account:
    def __init__(self, balance, account_holder):
        self.__balance = int(balance)
        self._account_holder = account_holder

    @property
    def __get_balance(self):
        return f'Your balance is {self.__balance}$!'

    @__get_balance.setter
    def __get_balance(self, num):
        if num > 0:
            self.__balance = num
        else:
            print('Your balance cannot be <0')

    @property
    def _get_account_holder(self):
        return self._account_holder

account = Account(100, 'Vlad')

try:
    print(account._Account__get_balance)
except AttributeError:
    print("Cannot access private method.")

print(account._account_holder)

try:
    account._Account__get_balance = 150
    print(account._Account__get_balance)
except AttributeError:
    print("Cannot access private method.")

try:
    account._Account__get_balance = -50
    print(account._Account__get_balance)
except AttributeError:
    print("Cannot access private method.")
