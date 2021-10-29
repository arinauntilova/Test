# 13-ROTATED_FLOWS
# 14-HEAT_TRANSFER_IN_SOLID
# 15-JOULE_HEATING_IN_SOLID

import os
import glob
import re

FILE_EXTENSION = ".stdout"
WORD = "error"
STRING_BEGIN = 'Solver finished at'

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
        found_files.append(name.replace(dir_name + '\\', ''))                                      
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

 # Проверить, что в файле нет определенного слова
def check_entry_word(dir_name, file_res):
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        with open(name) as file:
            cnt = 0
            for line in file:
                cnt += 1
                if WORD in line.lower():                                                               
                    file_res.write(name.replace(dir_name + '\\', '') + f'({str(cnt)}): ' + line)


 # Проверить, что в файле есть строка, начинающаяся с определенной фразы
def check_string_start(dir_name, file_res):
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        with open(name) as file:
            flag = False
            for line in file:
                if line.startswith(STRING_BEGIN):
                    flag = True
                    break

            if flag == False:
                file_res.write(name.replace(dir_name + '\\', '') + ': missing ' + f"'{STRING_BEGIN}' \n")


def find_max_value(dir_name):
    max_vals = {}
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        with open(name) as file:
            max_val = -1
            for line in file:
                if "Memory Working Set Current" in line and "Memory Working Set Peak" in line:
                    val = re.findall('Memory Working Set Peak = (\d*\.\d+|\d+)', line)
                    if float(val[0]) > max_val:
                        max_val = float(val[0])
            max_vals[name.replace(dir_name + '\\', '')] =  max_val
    return max_vals

def check_max_val(file):
    vals_run = find_max_value("ft_run")
    vals_ref = find_max_value("ft_reference")
    for key in vals_run.keys():
        val_run = vals_run.get(key)
        val_ref = vals_ref.get(key)
        diff = abs(val_run - val_ref) / min(val_ref, val_run)
        if diff > 0.5:
            print(diff)
            file.write(key + f" different 'Memory Working Set Peak' (ft_run={val_run}, \
                          ft_reference={val_ref}, rel.diff={round(diff, 2)}, criterion=0.5) \n")


def check_test_dir(test):
    os.chdir(test)
    file = open('report.txt', 'w');
    # Проверить, что папки ft_run и ft_reference существуют
    if not check_existence_dirs(file):
        return

    # Проверить, что в папках ft_run и ft_reference совпадает набор файлов "*.stdout"
    if not check_extra_miss_files(file):
        return

    # Проверить, что в файле нет слова ERROR
    check_entry_word("ft_run", file)
    # Проверить, что в файле есть строка, начинающаяся с 'Solver finished at'
    check_string_start("ft_run", file)

    #  Проверить, что max число Memory Working Set Peak из всего лога отличается не более чем на 50% 
    # (по отношению значения из ft_run к значению из ft_reference)
    check_max_val(file)


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
