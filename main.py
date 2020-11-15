# This is a sample Python script.
"""
pip install matplotlib
"""
import matplotlib.pyplot as plt
import math
import subprocess
import statistics
import re
"""
Идея оценки очень проста. Проверяется, насколько экспериментальные данные F1(N) 
соответствуют виду,например, степенной функции(О(N^X) polynomial) F(N) = K * N^P. 
Показатель степени P подбирается опытным путем, исходя из предварительного анализа 
трудоемкости программы: в нашем случае простая упорядоченная вставка должны давать 
квадратичную зависимость. 
Коэффициент пропорциональности K подбирается таким образом, чтобы значения 
экспериментальной и математической зависимости совпали в некоторой точке (N0) – 
можно взять одну из первых точек N0=5000, тогда F1(N0) = F(N0) = K * N0^P, откуда следует, 
что K = F1(N0) / N0^P.    
В общем виде K = F1(N0) / основную функцию O-нотаций 
Важна лишь асимптотическая сложность, т. е. сложность при стремлении размера входных данных к бесконечности.
"""


"""
О(1). constant time
О(log N). logarithmic
О(N). linear
О(N log N).quasilinear 
О(N^2). quadratic
О(N^X). polynomial
О(X^N). exponential
О(N!). factorial
"""
analytically_defined_functions = {
    # 'constant':
    'logarithmic': lambda mv: logarithmic(mv),
    'linear': lambda mv: linear(mv),
    'quasilinear': lambda mv: quasilinear(mv),
    # 'quadratic':
    'polynomial': lambda mv: polynomial(mv),
    # 'exponential':
    # 'factorial':
}


def logarithmic(mv):
    #  количество элементов
    n = mv[0][0]
    #  измеенное значение времени обработки этого количества
    f1_n = mv[0][2]
    c1_n = mv[0][1]
    # Коэффициент пропорциональности
    kt = f1_n / math.log(n, 2)
    kc = c1_n / math.log(n, 2)
    # перечень отклонений по всем точкам
    V = []
    # значеня функции
    FN =  []
    CN = []
    # аналитическая функция для сопоставления с измерениями
    f = lambda k, n: k * math.log(n, 2)

    # для каждой точки
    for n, _, f1_n in mv:
        # теоретическое значение времени выполнения полученное как функция от количества элементов n
        f_n = f(kt, n)
        c_n = f(kc, n)
        # отклонение теоретического значения от измеренного
        v = (f_n - f1_n) / f1_n
        V.append(v)
        FN.append(f_n)
        CN.append(c_n)

    # среднее отклоненние
    average_v = statistics.mean(V)

    return (average_v, 'logarithmic', 0.0, FN, CN)


def linear(mv):
    #  количество элементов
    n = mv[0][0]
    #  измеенное значение времени обработки этого количества
    f1_n = mv[0][2]
    c1_n = mv[0][1]
    # Коэффициент пропорциональности
    kt = f1_n / n
    kc = c1_n / n
    # перечень отклонений по всем точкам
    V = []
    # значеня функции
    FN = []
    CN = []
    # аналитическая функция для сопоставления с измерениями
    f = lambda k, n: k * n

    # для каждой точки
    for n, _, f1_n in mv:
        # теоретическое значение времени выполнения полученное как функция от количества элементов n
        f_n = f(kt, n)
        c_n = f(kc, n)
        # отклонение теоретического значения от измеренного
        v = (f_n - f1_n) / f1_n
        V.append(v)
        FN.append(f_n)
        CN.append(c_n)

    # среднее отклоненние
    average_v = statistics.mean(V)

    return (average_v, 'linear', 0.0, FN, CN)


def quasilinear(mv):
    #  количество элементов
    n = mv[0][0]
    #  измеенное значение времени обработки этого количества
    f1_n = mv[0][2]
    c1_n = mv[0][1]
    # Коэффициент пропорциональности
    kt = f1_n / (n * math.log(n, 2))
    kc = c1_n / (n * math.log(n, 2))
    # перечень отклонений по всем точкам
    V = []
    # значеня функции
    FN = []
    CN = []
    # аналитическая функция для сопоставления с измерениями
    f = lambda k, n: k * n * math.log(n, 2)

    # для каждой точки
    for n, _, f1_n in mv:
        # теоретическое значение времени выполнения полученное как функция от количества элементов n
        f_n = f(kt, n)
        c_n = f(kc, n)
        # отклонение теоретического значения от измеренного
        v = (f_n - f1_n) / f1_n
        V.append(v)
        FN.append(f_n)
        CN.append(c_n)

    # среднее отклоненние
    average_v = statistics.mean(V)

    return (average_v, 'quasilinear', 0.0, FN, CN)

poly_FN = []
poly_CN = []
# polynomial and quadratic
def polynomial(mv):
    global poly_FN
    global poly_CN

    # участок поиска
    # a <= p <= b
    a = 1.75
    b = 10
    # до какой точности будем искать
    epsilon = 0.02
    # найти подходящую степень
    p_opt = goldensection(polynomial_operating_time_costs, mv, a, b, epsilon)

    # получить отклонение для функции и найденной степени
    average_v = polynomial_operating_time_costs(mv, p_opt)

    # найти подходящую степень
    p_opt = goldensection(polynomial_number_of_operations_costs, mv, a, b, epsilon)
    polynomial_number_of_operations_costs(mv, p_opt)

    fit_function = 'polynomial'

    # если степень меньше куба, то это геометрическая зависимость
    if p_opt < 3:
        fit_function = 'quadratic'

    return (average_v, fit_function, p_opt, poly_FN, poly_CN)


# polynomial and quadratic
# функция для одномерной оптимизации g(x)
def polynomial_operating_time_costs(mv, p):
    global poly_FN
    poly_FN = []

    #  количество элементов
    n = mv[0][0]
    #  измеенное значение времени обработки этого количества
    f1_n = mv[0][2]
    # Коэффициент пропорциональности
    k = f1_n / math.pow(n, p)
    # перечень отклонений по всем точкам
    V = []
    # аналитическая функция для сопоставления с измерениями
    f = lambda k, p, n: k * math.pow(n, p)

    for n, _, f1_n in mv:
        # теоретическое значение времени выполнения полученное как функция от количества элементов n
        f_n = f(k, p, n)
        # отклонение теоретического значения от измеренного
        v = (f_n - f1_n) / f1_n
        V.append(v)
        poly_FN.append(f_n)

    # среднее отклоненние
    average_v = statistics.mean(V)

    return average_v

# трудозатраты
def polynomial_number_of_operations_costs(mv, p):
    global poly_CN

    poly_CN = []

    #  количество элементов
    n = mv[0][0]
    #  измеенное значение счетчика
    c1_n = mv[0][1]
    # Коэффициент пропорциональности
    k = c1_n / math.pow(n, p)
    # перечень отклонений по всем точкам
    V = []
    # аналитическая функция для сопоставления с измерениями
    f = lambda k, p, n: k * math.pow(n, p)

    for n, _, _ in mv:
        # теоретическое значение времени выполнения полученное как функция от количества элементов n
        c_n = f(k, p, n)
        # отклонение теоретического значения от измеренного
        v = (c_n - c1_n) / c1_n
        V.append(v)
        poly_CN.append(c_n)

    # среднее отклоненние
    average_v = statistics.mean(V)

    return average_v


def goldensection(g, args, a0, b0, epsilon):
    """
    Golden section or golden ratio algorithm
    :param g: one dimensional function for optimizing
    :param args: non volatile function's params
    :param a0: low optimization limit
    :param b0: high optimization limit
    :param epsilon: accuracy or measure
    :return:
    """
    # Номер шага
    k = 0

    # Отклонение от середины отрезка влево, вправо
    left = 0.0
    right = 0.0

    # Точка минимума
    x_min = 0.0

    # Отрезок локализации минимума
    ak = a0
    bk = b0

    # Пропорция золотого сечения
    # L / m = m / n
    # L = 1 - это целый отрезок
    # m = (-1+sqrt(5))/2 = 0,618*L - это бОльшая часть
    # n = L - m = 0,382 * L - это меньшая часть
    m = (-1.0 + math.sqrt(5.0)) / 2.0
    n = 1.0 - m

    niterations = 200
    k = 1
    #   Пока длина отрезка больше заданной точности
    while (bk - ak) >= epsilon and k < niterations:
        k += 1

        # Деллим отрезок в пропрорции золотого сечения
        left = ak + (bk - ak) * n
        right = ak + (bk - ak) * m

        # Проверяем в какую часть попадает точка минимума
        # слева от разбиения или справа и выбираем соответствующую точку
        if abs(g(args, left)) <= abs(g(args, right)):
            # Теперь правая граница отрезка локализации равна right
            bk = right
        else:
            # Теперь левая граница отрезка локализации равна left
            ak = left

    # точка как серединка полученного отрезочка a b
    x_min = (ak + bk) / 2.0

    return x_min


def print_hi():
    print('''
    ╔══════════════════╦═════════════════╗
    ║       Name       ║ Time Complexity ║
    ╠══════════════════╬═════════════════╣
    ║ Constant Time    ║       O(1)      ║
    ╠══════════════════╬═════════════════╣
    ║ Logarithmic Time ║     O(log n)    ║
    ╠══════════════════╬═════════════════╣
    ║ Linear Time      ║       O(n)      ║
    ╠══════════════════╬═════════════════╣
    ║ Quasilinear Time ║    O(n log n)   ║
    ╠══════════════════╬═════════════════╣
    ║ Quadratic Time   ║      O(n^2)     ║
    ╠══════════════════╬═════════════════╣
    ║ Polynomial Time  ║      О(N^X)     ║
    ╠══════════════════╬═════════════════╣
    ║ Exponential Time ║      O(2^n)     ║
    ╠══════════════════╬═════════════════╣
    ║ Factorial Time   ║       O(n!)     ║
    ╚══════════════════╩═════════════════╝
    ''')


def linear_test():
    print('Run \'Linear Time\' program and measure...\n')
    # запустить тест для имитатора линейного(linear) времении
    result = subprocess.run(['./linear'], stdout=subprocess.PIPE)
    raw = str(result.stdout.decode('utf-8'))
    raw = re.split(r"\n", raw)

    # экспериментальные данные
    measured_values = []
    for row in raw:
        if len(row) < 3:
            continue

        val = row.split('\t')
        measured_values.append((int(val[0]), int(val[1]), int(val[2])))

    # наименьшее отклонение
    var_opt = 1e99
    # наиболее подходящая аналитическая зависимость
    most_fit_function = None

    n = [n for n, _, _ in measured_values]
    f1_n = [f1_n for _, _, f1_n in measured_values]
    c1_n = [c1_n for _, c1_n, _ in measured_values]
    f_n = []
    c_n = []

    # опредилить наиболее подходящую аналитическую функцию
    for f in analytically_defined_functions:
        average_v, fit, _, fn, cn = analytically_defined_functions[f](measured_values)
        print(f'\ttrying {f} -> var:{average_v}%')

        # запомнить лучшее отклонение
        if abs(var_opt) > abs(average_v):
            var_opt = average_v
            most_fit_function = fit
            f_n = fn
            c_n = cn

    print(f'\nThe fittest function is {most_fit_function} time with variance {var_opt}%\n\n')

    plt.subplot(121)
    plt.plot(n, f1_n, "-r", label="measured")
    plt.plot(n, f_n, "-b", label="model")
    plt.legend()
    plt.xlabel("N, quantity")
    plt.ylabel("Time, ms")
    plt.grid(True)
    plt.subplot(122)
    plt.plot(n, c1_n, "--r", label="measured")
    plt.plot(n, c_n, "--b", label="model")
    plt.legend()
    plt.xlabel("N, quantity")
    plt.ylabel("Number of operations, quantity")
    plt.grid(True)
    plt.show()


def quasilinear_test():
    print('Run \'Quasilinear Time\' program and measure...\n')
    # запустить тест для имитатора квазилинейного(quasilinear) времении
    result = subprocess.run(['./quasilinear'], stdout=subprocess.PIPE)
    raw = str(result.stdout.decode('utf-8'))
    raw = re.split(r"\n", raw)

    # экспериментальные данные
    measured_values = []
    for row in raw:
        if len(row) < 3:
            continue

        val = row.split('\t')
        measured_values.append((int(val[0]), int(val[1]), int(val[2])))

    # наименьшее отклонение
    var_opt = 1e99
    # наиболее подходящая аналитическая зависимость
    most_fit_function = None

    n = [n for n, _, _ in measured_values]
    f1_n = [f1_n for _, _, f1_n in measured_values]
    c1_n = [c1_n for _, c1_n, _ in measured_values]
    f_n = []
    c_n = []

    # опредилить наиболее подходящую аналитическую функцию
    for f in analytically_defined_functions:
        average_v, fit, _, fn, cn = analytically_defined_functions[f](measured_values)
        print(f'\ttrying {f} -> var:{average_v}%')

        # запомнить лучшее отклонение
        if abs(var_opt) > abs(average_v):
            var_opt = average_v
            most_fit_function = fit
            f_n = fn
            c_n = cn

    print(f'\nThe fittest function is {most_fit_function} time with variance {var_opt}%\n\n')

    plt.subplot(121)
    plt.plot(n, f1_n, "-r", label="measured")
    plt.plot(n, f_n, "-b", label="model")
    plt.legend()
    plt.xlabel("N, quantity")
    plt.ylabel("Time, ms")
    plt.grid(True)
    plt.subplot(122)
    plt.plot(n, c1_n, "--r", label="measured")
    plt.plot(n, c_n, "--b", label="model")
    plt.legend()
    plt.xlabel("N, quantity")
    plt.ylabel("Number of operations, quantity")
    plt.grid(True)
    plt.show()

    
def quadratic_test():
    print('Run \'Quadratic Time\' program and measure...\n')
    # запустить тест для имитатора геометрического(quadratic) времении
    result = subprocess.run(['./quadratic'], stdout=subprocess.PIPE)
    raw = str(result.stdout.decode('utf-8'))
    raw = re.split(r"\n", raw)

    # экспериментальные данные
    measured_values = []
    for row in raw:
        if len(row) < 3:
            continue

        val = row.split('\t')
        measured_values.append((int(val[0]), int(val[1]), int(val[2])))

    # наименьшее отклонение
    var_opt = 1e99
    # наиболее подходящая аналитическая зависимость
    most_fit_function = None
    # найденная степерь для геометрических и полиномиальных зависимостей
    p_opt = 0.0

    n = [n for n, _, _ in measured_values]
    f1_n = [f1_n for _, _, f1_n in measured_values]
    c1_n = [c1_n for _, c1_n, _ in measured_values]
    f_n = []
    c_n = []

    # опредилить наиболее подходящую аналитическую функцию
    for f in analytically_defined_functions:

        average_v, fit, p_opt, fn, cn = analytically_defined_functions[f](measured_values)
        print(f'\ttrying {f} -> var:{average_v}%')

        # запомнить лучшее отклонение
        if abs(var_opt) > abs(average_v):
            var_opt = average_v
            most_fit_function = fit
            f_n = fn
            c_n = cn

    print(f'\nThe fittest function is {most_fit_function} time with variance {var_opt}% and power {p_opt}\n\n')

    plt.subplot(121)
    plt.plot(n, f1_n, "-r", label="measured")
    plt.plot(n, f_n, "-b", label="model")
    plt.legend()
    plt.xlabel("N, quantity")
    plt.ylabel("Time, ms")
    plt.grid(True)
    plt.subplot(122)
    plt.plot(n, c1_n, "--r", label="measured")
    plt.plot(n, c_n, "--b", label="model")
    plt.legend()
    plt.xlabel("N, quantity")
    plt.ylabel("Number of operations, quantity")
    plt.grid(True)
    plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

    linear_test()

    quasilinear_test()

    quadratic_test()


