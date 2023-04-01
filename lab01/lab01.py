import argparse
import random


def remove_even_chains(A, B):
    # удаляем из списка A цепочки четных элементов, содержащие элементы из списка B
    i = 0
    while i < len(A):
        if A[i] % 2 == 0:
            chain_start = i
            while i < len(A) and A[i] % 2 == 0:
                i += 1
            chain_end = i - 1
            if any(x in B for x in A[chain_start:chain_end+1]):
                del A[chain_start:chain_end+1]
                i = chain_start
        else:
            i += 1


def get_list_from_input():
    while True:
        lst = input().replace(",", " ").split()  # разделяем строку по пробелам и запятым
        try:
            lst = [int(x) for x in lst]
            return lst
        except ValueError:
            print("Ошибка: введены некорректные данные, необходимо ввести числа через запятую или пробел.")


def get_random_list(n):
    # получение списка случайных чисел
    lst = [random.randint(1, 20) for _ in range(n)]
    return lst


# Разбор аргументов командной строки
parser = argparse.ArgumentParser(description="Удаление цепочек четных элементов из списка A, содержащих элементы из списка B")
parser.add_argument("-m", "--manual", action="store_true", help="ввод списка A и B в интерактивном режиме")
parser.add_argument("-nA", "--length_a", type=int, help="длина списка A при генерации случайным образом")
parser.add_argument("-nB", "--length_b", type=int, help="длина списка B при генерации случайным образом")
args = parser.parse_args()

if args.manual:
    print("Введите элементы списка A (пустая строка для завершения ввода):")
    A = get_list_from_input()

    print("Введите элементы списка B (пустая строка для завершения ввода):")
    B = get_list_from_input()

elif args.length_a and args.length_b:
    A = get_random_list(args.length_a)
    B = get_random_list(args.length_b)
else:
    print("Необходимо выбрать способ ввода списка, используя аргументы командной строки")
    parser.print_help()
    exit(1)

print("Список A:", A)
print("Список B:", B)

# Удаляем цепочки четных элементов, содержащие элементы из списка B
remove_even_chains(A, B)

# Выводим результат
print("Результат:", A)
