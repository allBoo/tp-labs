import numpy as np
import argparse


# создание парсера аргументов командной строки
parser = argparse.ArgumentParser()
parser.add_argument('-N', type=int, required=True, help='количество строк матрицы')
parser.add_argument('-M', type=int, required=True, help='количество столбцов матрицы')
args = parser.parse_args()

N = args.N
M = args.M

# генерация матрицы случайных чисел размера N x M
A = np.random.rand(N, M)

# вычисление суммы элементов матрицы
sum_A = np.sum(A)

# вычисление суммы элементов каждого столбца
sum_cols = np.sum(A, axis=0)

# вычисление доли каждого столбца в сумме элементов всей матрицы
fractions = sum_cols / sum_A

# создание новой матрицы, содержащей исходную матрицу и доли каждого столбца
B = np.vstack((A, fractions))

# выводим в консоль как есть
print(f'Матрица A ({N}x{M}):\n{A}\n\n')
print(f'Сумма элементов матрицы A: {sum_A}\n\n')
print(f'Суммы элементов каждого столбца: {sum_cols}\n\n')
print(f'Доли каждого столбца в сумме элементов матрицы: {fractions}\n\n')
print(f'Матрица B ({N+1}x{M}):\n{B}')

# исходную матрицу и результат сохраняем красиво в файл
np.savetxt('input.txt', A, fmt="%.6f")
np.savetxt('output.txt', B, fmt="%.6f")
