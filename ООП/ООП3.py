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
    def get_balance(self):
        return f'Your balance is {self.__balance}$!'

    @get_balance.setter
    def get_balance(self, num):
        if num > 0:
            self.__balance = num
        else:
            print('Your balance cannot be <0')

    @property
    def _get_account_holder(self):
        return self._account_holder

account = Account(100, 'Vlad')

print(account.get_balance)
print(account._account_holder)

account.get_balance = 150
print(account.get_balance)

account.get_balance = -50
print(account.get_balance)
