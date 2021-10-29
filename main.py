# 13-ROTATED_FLOWS
# 14-HEAT_TRANSFER_IN_SOLID
# 15-JOULE_HEATING_IN_SOLID

import os
import glob

FILE_EXTENSION = ".stdout"
WORD = "error"
STRING_BEGIN = 'Solver finished at'

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
    flag = True
    if not (os.path.exists('ft_run')):
        file.write("directory missing: ft_run \n")
        flag = False
    if not (os.path.exists('ft_reference')):
        file.write("directory missing: ft_reference \n")
        flag = False
    return flag
    

def check_set_of_files(dir_name):
    found_files = []
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        # print(name)
        found_files.append(name.replace(dir_name + '\\', ''))                                      
    # print(found_files)
    return found_files

def check_extra_miss_files(file):
    ft_run_files = set(check_set_of_files("ft_run"))
    ft_reference_files = set(check_set_of_files("ft_reference"))

    flag = True
    # множество из всех элементов  ft_reference, не принадлежащие ft_run                     
    res = ft_reference_files.difference(ft_run_files)
    if res:
        file.write("In ft_run there are missing files present in ft_reference: " + ', '.join(list(res)) + '\n')
        flag = False

    # множество из всех элементов ft_run, не принадлежащие ft_reference
    res = ft_run_files.difference(ft_reference_files)
    if res:
        file.write("In ft_run there are extra files not present in ft_reference: " + ', '.join(list(res)) + '\n')
        flag = False

    return flag

def check_entry_word(dir_name, file_res):
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        with open(name) as file:
            cnt = 0
            for line in file:
                cnt += 1
                if WORD in line.lower():
                    # print("Error found!\n")
                    file_res.write(name.replace(dir_name + '\\', '') + f'({str(cnt)}): ' + line + '\n')


def check_string_start(dir_name, file_res):
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        with open(name) as file:
            flag = False
            for line in file:
                if line.startswith(STRING_BEGIN):
                    flag = True
                    break

            if flag == False:
                # print('Line not found!\n')
                file_res.write(name.replace(dir_name + '\\', '') + ': missing ' + f"'{STRING_BEGIN}' \n")

def check_test_dir(test):
    os.chdir(test)
    file = open('report.txt', 'w');
    # Проверить, что папки ft_run и ft_reference существуют.
    if not check_existence_dirs(file):
        return

    # Проверить, что в папках ft_run и ft_reference совпадает набор файлов "*.stdout".
    if not check_extra_miss_files(file):
        return

    # Проверить, что в файле нет слова ERROR
    check_entry_word("ft_run", file)
    # Проверить, что в файле есть строка, начинающаяся с 'Solver finished at'
    check_string_start("ft_run", file)

    file.close()

def get_all_dirs(dirs):
    for dir in dirs:     
        os.chdir(dir)
        dir_test_results = os.listdir(".")
        for test in dir_test_results:
            check_test_dir(test)
            os.chdir('../')

        os.chdir('../')

# папки из папки logs
# получение списка папок в каталоге
dir_tasks = os.listdir()  # extend
print(dir_tasks)

print(dir_tasks)

get_all_dirs(dir_tasks)
