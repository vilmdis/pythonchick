# def square(x):
#     return x ** 2
# old_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# new_list = list(map(square, old_list))
# print(new_list)

# def valid(x):
#     return x % 2 == 0

# list3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# result = list(filter(valid, list3))
# print(result)

# from functools import reduce

# def add(x, y):
#     return x + y

# list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# res = reduce(add, list1)
# print(res)

# def len1(x, y):
#     return x if len(x) > len(y) else y

# list2 = ['apple', 'banana', 'watermalon', 'orange', 'carrot']
# res1 = reduce(len1, list2)
# print(res1)

# res = lambda x, y: x * y
# print(res(12, 23))

# def merge_dicts(dict1, dict2):
#     merged_dict = dict1.copy()
#     merged_dict.update(dict2)
#     return merged_dict

# dict1 = {'імя': 'Іван', 'прізвище': 'Петров', 'вік': 25}
# dict2 = {'телефон': '123-456-7890', 'email': 'ivan@example.com', 'стать': 'чоловіча'}

# merged_dict = merge_dicts(dict1, dict2)
# print(merged_dict)

# def len_ip(ip):
#     if ip.split() < 256:
#         return 'Valid'
#     else:
#         return 'No valid'
# ip = input()
# print(len_ip(ip))

# def index(list):
#     list.split()
#     for i in len(list):
#         if i == 5:
#             return i
#         else:
#             pass
# list = input()
# print(index(list))

# def search(sentence):
#     if ' ' in sentence:
#         return 'No valid'
#     else:
#         return 'Valid'
# sentence = input()
# print(search(sentence))

# import re

# txt = input()
# if re.match(r'^[A-Za-z]+$', txt):
#     print('Valid')
# else:
#     print('No valid')

# import re

# txt = input()
# if re.match(r'\d+$', txt):
#     print('Valid')
# else:
#     print('No valid')

# import re

# txt = input()
# search_num = re.findall(r'\b\d{5}\b', txt)
# print(search_num)

# import re

# txt = input()
# if re.match(r'^[0-3][1-1]+-[0-1][1-2]+-\d{4}$', txt):
#     print('Valid')
# else:
#     print('No valid')

# import re

# txt = '+380 99 321-9384'
# if re.match(r'^\+380 \d{2} \d{3}-\d{4}$', txt):
#     print('Valid')
# else:
#     print('No valid')

# import re

# txt = 'assassasa@gmail.com'
# if re.match(r'\b[a-zA-Z]+@gmail\.com\b', txt):
#     print('Valid')
# else:
#     print('No valid')
# або:
# import re

# txt = 'assassasa@gmail.com'
# if re.match(r'\b\w+@[a-z]+\.[a-z]+\b', txt):
#     print('Valid')
# else:
#     print('No valid')

# import re

# txt = '111.111.111.111'
# if re.match(r'\b[0-255]+\.[0-255]+\.[0-255]+\.[0-255]+\b', txt):
#     print('Valid')
# else:
#     print('No valid')

# def count_down(x):
#     for i in range(x, -1, -1):
#         yield i
# for num in count_down(10):
#     print(num)

# x = int(input())
# res = [i for i in range(x, -1, -1)]
# print(res)

# class RangeIterator:

#     def __init__(self, start, end, step):
#         self.start = start
#         self.end = end
#         self.step = step

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.start >= self.end:
#             raise StopIteration
#         value = self.start
#         self.start += self.step
#         return value

# for i in RangeIterator(1, 10, 2):
#     print(i)

# class CyclicIterator:

#     def __init__(self, iterable):
#         self.iterable = iterable
#         self.iterator = iter(iterable)
#         self.next_v = next(self.iterator)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         x = self.next_v
#         try:
#             self.next_v = next(self.iterator)
#         except StopIteration:
#             self.iterator = iter(self.iterable)
#             self.next_v = next(self.iterator)
#         return x
#     def peek(self):
#         return self.next_v

# for i in CyclicIterator([1, 2, 3]):
#     print(i)

# cycle_iter = CyclicIterator([1, 2, 3])
# print(next(cycle_iter))
# print(cycle_iter.peek())
# print(next(cycle_iter))

# class FilterIterator:

#     def __init__(self, iterable, predicate):
#         self.iterator = iter(iterable)
#         self.predicate = predicate

#     # def __iter__(self):
#     #     return self

#     def __next__(self):
#         while True:
#             item = next(self.iterator)
#             if self.predicate(item):
#                 return item

# f_iter = FilterIterator([1, 2, 3, 4], lambda x: x % 2 == 0)

# while True:
#     try:
#         print(next(f_iter))
#     except StopIteration:
#         break
