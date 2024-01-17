import os

filename = 'text.txt'
abs_path = os.path.abspath(__file__)
print(abs_path)
# абсолютний шлях

base_dir = os.path.dirname(abs_path)
print(base_dir)
# абсолютний шлях до директорії пайтончик

file_path = os.path.join(base_dir, 'files', filename)
print(file_path)
# конкатинує всі передані значення

f = open(file_path, 'r')
print(f.read())
f.close()


filename = 'files/text.txt'

f = open(filename, 'a+')
f.write('\nFUCK')
f.seek(0)
print(f.read())
f.close()
