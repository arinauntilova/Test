import os
import glob
import re

FILE_EXTENSION = ".stdout"
WORD = "error"
STRING_BEGIN = 'Solver finished at'
MEMORY_CRITERION = 0.5
TOTAL_CRITERION = 0.1

os.chdir('task1\logs')

# Проверка, что папки ft_run и ft_reference существуют.
def check_existence_dirs(file):
    flag = True
    if not (os.path.exists('ft_run')):
        file.write("directory missing: ft_run")
        flag = False
    if not (os.path.exists('ft_reference')):
        file.write("directory missing: ft_reference")
        flag = False
    return flag

# Поиск всех файлов нужного расширения в указанной директории
def check_set_of_files(dir_name, extension):
    found_files = []
    for name in sorted(glob.glob(dir_name + "\**\*" + extension, recursive = True)):
        # В названии файла оставляем только название файла и одной родительской директории
        found_files.append(name.replace(dir_name + '\\', ''))                                      
    return found_files

# Проверка, что в папках ft_run и ft_reference совпадает набор файлов с указанным расширением
def check_extra_miss_files(file, extension):
    ft_run_files = set(check_set_of_files("ft_run", extension))
    ft_reference_files = set(check_set_of_files("ft_reference", extension))

    flag = True
    # множество из всех элементов  ft_reference, не принадлежащие ft_run                     
    res = ft_reference_files.difference(ft_run_files)
    if res:
        file.write("In ft_run there are missing files present in ft_reference: " + ', '.join(list(res)))
        flag = False

    # множество из всех элементов ft_run, не принадлежащие ft_reference
    res = ft_run_files.difference(ft_reference_files)
    if res:
        file.write("In ft_run there are extra files not present in ft_reference: " + ', '.join(list(res)))
        flag = False

    return flag

 # Проверка, что в файле нет определенного слова
def check_no_entry_word(dir_name, file_res, word):
    flag = True
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        with open(name) as file:
            cnt = 0
            for line in file:
                cnt += 1
                if word in line.lower():                                                               
                    file_res.write(name.replace(dir_name + '\\', '') + f'({str(cnt)}): ' + line[:-1])
                    flag = False
    return flag


 # Проверка, что в файле есть строка, начинающаяся с определенной фразы
def check_string_start(dir_name, file_res, string_beg):
    for name in sorted(glob.glob(dir_name + "\**\*" + FILE_EXTENSION, recursive = True)):
        with open(name) as file:
            flag = False
            for line in file:
                if line.startswith(string_beg):
                    flag = True
                    break
            if flag == False:
                file_res.write(name.replace(dir_name + '\\', '') + ': missing ' + f"'{string_beg}'")
    return flag

# Поиск max значения Memory Working Set Peak в файлах указанного расширения
# выход: множество пар ключ-значение для каждого проекта вида имя файла : max_значение
def find_max_memory_value(dir_name, extension):
    max_vals = {}
    for name in sorted(glob.glob(dir_name + "\**\*" + extension, recursive = True)):
        with open(name) as file:
            max_val = -1
            for line in file:
                if "Memory Working Set Current" in line and "Memory Working Set Peak" in line:
                    # Поиск вещественного числа после 'Memory Working Set Peak'
                    val = re.findall('Memory Working Set Peak = (\d*\.\d+)', line)
                    if float(val[0]) > max_val:
                        max_val = float(val[0])
            max_vals[name.replace(dir_name + '\\', '')] = max_val
    return max_vals

# Поиск последнего значения Total в файлах указанного расширения
# выход: множество пар ключ-значение для каждого проекта вида имя файла : значение total
def find_total_value(dir_name, extension):
    total_vals = {}
    for name in sorted(glob.glob(dir_name + "\**\*" + extension, recursive = True)):
        with open(name) as file:
            for line in file:
                if "MESH::Bricks: Total=" in line and " Gas=" in line and \
                            "Solid=" in line and "Partial=" in line:
                    # Поиск целого числа после 'Total'
                    val = re.findall('Total=(\d+)', line)
                    total_val = int(val[0])
            total_vals[name.replace(dir_name + '\\', '')] = total_val
    return total_vals

# Поиск значений атрибутов из ft_run, которые отличаются с ft_reference
# не более, на значение crit
# параметры: file - файл для записи результата проверки
#            find_func - функция для поиска нужного значения
#            crit - допустимая разница в значениях из ft_run к значению из ft_reference
#            attribute - атрибут, который проверяем (нужен для вывода в отчет о тесте)
def check_values(file, find_func, crit, attribute, extension):
    flag = True
    vals_run = find_func("ft_run", extension)
    vals_ref = find_func("ft_reference", extension)
    for key in vals_run.keys():
        val_run = vals_run.get(key)
        val_ref = vals_ref.get(key)
        # Вычисление разницы значения из ft_run к значению из ft_reference
        diff = abs(val_run - val_ref) / min(val_ref, val_run)
        if diff > crit:
            file.write(key + f" different '{attribute}' (ft_run={val_run}," +
                         f" ft_reference={val_ref}, rel.diff={round(diff, 2)}, criterion={crit})")
            flag = False
    return flag
            
# Проверка одной директории с тестом
def check_test_dir(file):
    flag = True

    # Проверка, что папки ft_run и ft_reference существуют
    if not check_existence_dirs(file):
        return False

    # Проверка, что в папках ft_run и ft_reference совпадает набор файлов "*.stdout"
    if not check_extra_miss_files(file, FILE_EXTENSION):
        return False

    # Проверка, что в файле нет слова ERROR
    flag &= check_no_entry_word("ft_run", file, WORD)

    # Проверка, что в файле есть строка, начинающаяся с 'Solver finished at'
    flag &= check_string_start("ft_run", file, STRING_BEGIN)

    #  Проверка, что max число Memory Working Set Peak из всего лога отличается 
    # не более, чем на 50% (по отношению значения из ft_run к значению из ft_reference)
    flag &= check_values(file, find_max_memory_value, MEMORY_CRITERION, \
                                    "Memory Working Set Peak", FILE_EXTENSION)
    
    #  Проверка, что последнее значение Total из всего лога отличается 
    # не более чем на 10% (по отношению значения из ft_run к значению из ft_reference)
    flag &= check_values(file, find_total_value, TOTAL_CRITERION, "Total", FILE_EXTENSION)

    return flag

# Получение информации о всех тестах
def get_all_dirs(dirs):
    # Имя файла для записи результата теста
    filename = 'report.txt'
    for dir in dirs:     
        os.chdir(dir)
        dir_test_results = os.listdir(".")
        for test in dir_test_results:
            os.chdir(test)
            file = open(filename, 'w');
            # Проверка одной директории с тестом
            flag = check_test_dir(file)
            file.close()
            path = os.getcwd()
            # разделяем путь к файлу, чтобы оставить только часть пусти внутри logs
            path = path.split('logs')[-1]
            if flag:
                print("OK: " + path)
            else:
                print("FAIL: " + path)
                with open(filename) as file:
                    print(file.read())          
            os.chdir('../')
        os.chdir('../')

# Получение списка папок в каталоге logs
dir_tasks = os.listdir() 

# Получение информации о всех тестах
get_all_dirs(dir_tasks)