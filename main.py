# 13-ROTATED_FLOWS
# 14-HEAT_TRANSFER_IN_SOLID
# 15-JOULE_HEATING_IN_SOLID

import os

FILE_EXTENSION = ".stdout"

# вывести текущую директорию
print("Текущая деректория:", os.getcwd())
# изменение текущего каталога на 'folder'
os.chdir("task1\logs")

# вывод текущей папки
print("Текущая директория изменилась на folder:", os.getcwd())

# распечатать все файлы и папки в текущем каталоге
print("Все папки и файлы:", os.listdir())

# Проверить, что папки ft_run и ft_reference существуют.
def check_existence_dirs(file):
    if not (os.path.exists('ft_run')):
        file.write("directory missing: ft_run \n")
    if not (os.path.exists('ft_reference')):
        file.write("directory missing: ft_reference \n")

def check_set_of_files():
    pass

def check_test_dir(test):
    os.chdir(test)
    file = open('report.txt', 'w');
    # Проверить, что папки ft_run и ft_reference существуют.
    check_existence_dirs(file)

    check_set_of_files()

    file.close()

def get_all_dirs(dirs):
    for dir in dirs:     
        os.chdir(dir)
        dir_test_results = os.listdir(".")
        for test in dir_test_results:
            # os.chdir(test)
            check_test_dir(test)
            os.chdir('../')

        os.chdir('../')

# папки из папки logs
# получение списка папок в каталоге
dir_tasks = os.listdir()  # extend
print(dir_tasks)

print(dir_tasks)

get_all_dirs(dir_tasks)
