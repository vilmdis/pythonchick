# import os

# filename = 'text.txt'
# abs_path = os.path.abspath(__file__)
# print(abs_path)
# # абсолютний шлях

# base_dir = os.path.dirname(abs_path)
# print(base_dir)
# # абсолютний шлях до директорії пайтончик

# file_path = os.path.join(base_dir, 'files', filename)
# print(file_path)
# # конкатинує всі передані значення

# f = open(file_path, 'r')
# print(f.read())
# f.close()


# filename = 'files/text.txt'

# f = open(filename, 'a+')
# f.write('\nFUCK')
# f.seek(0)
# print(f.read())
# f.close()

# with open('text.txt', 'a') as f:
#     f.write('\n Another line')

# class OpenFile:
#     def __init__(self, filename, mode):
#         self.filename = filename
#         self.mode = mode
#     def __enter__(self):
#         self.file = open(self.filename, self.mode)
#         return self.file
#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         self.file.close()

# with OpenFile('text.txt', 'w') as f:
#     f.write('Some other line')

# # or

# from contextlib import contextmanager

# @contextmanager
# def open_file(filename, mode):
#     try:
#         file = open(filename, mode)
#         yield file
#     finally:
#         file.close()

# with open_file('text.txt', 'w') as f:
#     f.write('Some data')


# from time import time

# from contextlib import contextmanager

# @contextmanager
# def code_time():
#     start = time()
#     try:
#         print('Code start.')
#         yield start
#         print('Code end.')
#     except Exception as e:
#         print(e)
#     finally:
#         end = time()
#         res = end - start
#         print(f'The code was executed by {res} sec.')

# with code_time():
#     def add(x, y):
#         return x + y
#     print(add(1760, 922))

# # or

# from time import time

# class TimerContextManager:
#     def __enter__(self):
#         self.start_time = time()
#         print('Code start')
#         return self

#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         end_time = time()
#         elapsed_time = end_time - self.start_time
#         print('Code end')
#         print(f"Код виконався успішно за {elapsed_time} секунд.")

# with TimerContextManager() as timer:
#     def add(x, y):
#         return x + y
#     print(add(1760, 922))

# from itertools import permutations
# # print(list(permutations([1, 2, 3])))

# def generate(list):
#     for permutation in permutations(list):
#         yield permutation

# list = [1, 2, 3]
# for combination in generate(list):
#   print(combination)

# def even_num(n):
#     for i in range(n):
#         if i % 2 == 0:
#             yield i

# even_list = even_num(5)

# print(next(even_list))

# def palin_num(n):
#     for num in range(0, n + 1):
#         num_str = str(num)
#         if num_str == num_str[::-1]:
#             yield num
# pal = palin_num(1000)
# print(next(pal))
# for palin in pal:
#     print(palin)

# filename = 'files/text.txt'

# f = open(filename, 'a+')
# f.write('\nFUCK')
# f.seek(0)
# print(f.read())
# f.close()

# with open('text.txt', 'a') as f:
#     f.write('\n Another line')

# with open('files/text.txt', 'r') as f:
#     word = 0
#     for i in f:
#         word += len(i.split())
#     print(word)

# with open('files/text.txt', 'a') as f:
#     x = input()
#     f.seek(0)
#     f.write(x + '\n')

# try:
#     numbers = input('Введіть числа через кому: ')
#     numb = [int(num) for num in numbers.split(',')]
#     print(numb)
# except ValueError as e:
#     print(e)
# except IndexError as e:
#     print(e)

# class FileOpen:
#     def __init__(self, filename, mode):
#         self.filename = filename
#         self.mode = mode
#     def __enter__(self):
#         self.file = open(self.filename, self.mode)
#         return self.file
#     def __exit__(self, exc_type, exc_value, exc_traceback):
#         self.file.close()

# with FileOpen("files/text.txt", "r") as f:
#     print(f.read())

# # or

# from contextlib import contextmanager

# @contextmanager
# def file_open(filename, mode):
#     try:
#         file = open(filename, mode)
#         yield file
#     except Exception as e:
#         print(e)
#     finally:
#         file.close()

# with file_open("files/text.txt", "r") as f:
#     print(f.read())
