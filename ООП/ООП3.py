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
        self._balance = int(balance)
        self._account_holder = account_holder

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, num):
        if num > 0:
            self._balance = num
        else:
            print('Your balance cannot be <0')

    @property
    def account_holder(self):
        return self._account_holder

    def return_bal(self):
        return f'Your balance is {self._balance}$!'

account = Account(100, 'Vlad')

print(account.balance)

print(account.account_holder)

print(account.return_bal())

account.balance = 150

print(account.return_bal())

account.balance = -50
