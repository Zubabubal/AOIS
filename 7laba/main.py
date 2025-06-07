def print_matrix(matrix, title="Исходная матрица"):
    """Печать матрицы"""
    print(f"{title}:")
    for row in matrix:
        print([f"{bit:1d}" for bit in row])
    print()


def read_word(matrix, word_index):
    """Считывание слова по индексу с диагональной адресацией"""
    word = []
    rows = len(matrix)
    cols = len(matrix[0])

    # Правильная формула для диагональной адресации
    start_col = (15 - word_index) % cols

    for i in range(rows):
        col = (start_col + i) % cols
        word.append(matrix[i][col])

    return word


def read_column(matrix, col_index):
    """Считывание разрядного столбца по индексу"""
    column = []
    for row in matrix:
        column.append(row[col_index])
    return column


def write_column(matrix, col_index, data):
    """Запись данных в разрядный столбец"""
    for i in range(len(matrix)):
        if i < len(data):
            matrix[i][col_index] = data[i]


def write_word(matrix, word_index, data):
    """Запись слова по индексу с диагональной адресацией"""
    rows = len(matrix)
    cols = len(matrix[0])

    # Правильная формула для диагональной адресации
    start_col = (15 - word_index) % cols

    for i in range(rows):
        if i < len(data):
            col = (start_col + i) % cols
            matrix[i][col] = data[i]


def logical_function_f5(a, b):
    """Логическая функция f5: b (согласно варианту 4)"""
    return b


def logical_function_f10(a, b):
    """Логическая функция f10: НЕ b (согласно варианту 4)"""
    return 1 - b


def logical_function_f0(a, b):
    """Логическая функция f0: 0"""
    return 0


def logical_function_f15(a, b):
    """Логическая функция f15: 1"""
    return 1


def apply_logical_function(word1, word2, func):
    """Применение логической функции к двум словам"""
    result = []
    for i in range(len(word1)):
        a = word1[i] if i < len(word1) else 0
        b = word2[i] if i < len(word2) else 0
        result.append(func(a, b))
    return result


def extract_fields(word):
    """Извлечение полей V(3), A(4), B(4), S(5) из 16-битного слова"""
    if len(word) < 16:
        word = word + [0] * (16 - len(word))

    V = word[0:3]  # первые 3 бита
    A = word[3:7]  # следующие 4 бита
    B = word[7:11]  # следующие 4 бита
    S = word[11:16]  # последние 5 бит

    return V, A, B, S


def binary_add(a_bits, b_bits):
    """Сложение двух двоичных чисел, представленных списками битов"""
    # Преобразуем в числа
    a = 0
    b = 0

    for i, bit in enumerate(reversed(a_bits)):
        a += bit * (2 ** i)

    for i, bit in enumerate(reversed(b_bits)):
        b += bit * (2 ** i)

    # Складываем
    result = a + b

    # Преобразуем обратно в биты (5 бит для результата)
    result_bits = []
    for i in range(5):
        result_bits.insert(0, (result >> i) & 1)

    return result_bits


def find_matching_words(matrix, target_v):
    """Поиск слов с заданным значением V"""
    matching_words = []

    for word_idx in range(16):
        word = read_word(matrix, word_idx)
        V, A, B, S = extract_fields(word)

        # Проверяем совпадение V с целевым значением
        if V == target_v:
            matching_words.append((word_idx, word, V, A, B, S))

    return matching_words


def arithmetic_operation(matrix, target_v):
    """Сложение полей Aj и Bj в словах Sj, у которых Vj совпадает с заданным V"""
    matching_words = find_matching_words(matrix, target_v)

    print(f"Арифметическая операция с фильтром V = {target_v}:")
    print("Найденные слова для обработки:")

    if not matching_words:
        print("Нет слов с заданным значением V")
        print()
        return matrix

    for word_idx, word, V, A, B, S in matching_words:
        print(f"Слово {word_idx}: V={V}, A={A}, B={B}, S={S}")

        # Складываем A и B
        new_S = binary_add(A, B)
        print(f"A + B = {new_S}")

        # Создаем новое слово
        new_word = V + A + B + new_S

        # Записываем обратно в матрицу
        write_word(matrix, word_idx, new_word)
        print(f"Новое слово {word_idx}: {new_word}")

    print()
    return matrix


def pattern_matching_search(matrix, target_pattern):
    """Поиск по соответствию с заданным образцом"""
    matches_info = []

    print(f"Поиск по соответствию с образцом: {target_pattern}")
    print("Анализ совпадений по словам:")

    # Проверяем каждое слово
    for word_idx in range(16):
        word = read_word(matrix, word_idx)

        # Подсчитываем совпадения
        matches = 0
        match_positions = []
        for i in range(min(len(word), len(target_pattern))):
            if word[i] == target_pattern[i]:
                matches += 1
                match_positions.append(i)

        matches_info.append((word_idx, word, matches, match_positions))
        print(f"Слово {word_idx}: {word}, совпадений: {matches}, позиции: {match_positions}")

    # Находим максимальное количество совпадений
    max_matches = max(info[2] for info in matches_info)
    best_matches = [(info[0], info[1]) for info in matches_info if info[2] == max_matches]

    return best_matches, max_matches


def main():
    # Исходная матрица 16x16
    matrix = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    print_matrix(matrix)

    # Демонстрация извлечения слов
    print("=== ДЕМОНСТРАЦИЯ ИЗВЛЕЧЕНИЯ СЛОВ ===")
    for i in [0, 1, 2, 3]:
        word = read_word(matrix, i)
        V, A, B, S = extract_fields(word)
        print(f"Слово {i}: {word}")
        print(f"  V={V}, A={A}, B={B}, S={S}")
    print()

    # Демонстрация извлечения столбцов
    print("=== ДЕМОНСТРАЦИЯ ИЗВЛЕЧЕНИЯ СТОЛБЦОВ ===")
    for i in [0, 1, 2, 3]:
        col = read_column(matrix, i)
        print(f"Столбец {i}: {col}")
    print()

    # Создаем копию исходной матрицы для логических операций
    matrix_logic = [row[:] for row in matrix]

    # Применение логических функций согласно варианту 4: f5 и f10, f0 и f15
    print("=== ЛОГИЧЕСКИЕ ОПЕРАЦИИ (ВАРИАНТ 4) ===")

    # f5 (b) между столбцами 0 и 1, результат в столбец 2
    print("Применение f5 (b) между столбцами 0 и 1, результат в столбец 2:")
    col0 = read_column(matrix_logic, 0)
    col1 = read_column(matrix_logic, 1)
    result_f5 = apply_logical_function(col0, col1, logical_function_f5)
    write_column(matrix_logic, 2, result_f5)
    print(f"Столбец 0: {col0}")
    print(f"Столбец 1: {col1}")
    print(f"Результат f5 (b): {result_f5}")
    print()

    # f10 (НЕ b) между столбцами 0 и 1, результат в столбец 3
    print("Применение f10 (НЕ b) между столбцами 0 и 1, результат в столбец 3:")
    result_f10 = apply_logical_function(col0, col1, logical_function_f10)
    write_column(matrix_logic, 3, result_f10)
    print(f"Столбец 0: {col0}")
    print(f"Столбец 1: {col1}")
    print(f"Результат f10 (НЕ b): {result_f10}")
    print()

    # f0 (константа 0) в столбец 4
    print("Применение f0 (константа 0) в столбец 4:")
    result_f0 = apply_logical_function(col0, col0, logical_function_f0)
    write_column(matrix_logic, 4, result_f0)
    print(f"Результат f0: {result_f0}")
    print()

    # f15 (константа 1) в столбец 5
    print("Применение f15 (константа 1) в столбец 5:")
    result_f15 = apply_logical_function(col0, col0, logical_function_f15)
    write_column(matrix_logic, 5, result_f15)
    print(f"Результат f15: {result_f15}")
    print()

    print_matrix(matrix_logic, "Матрица после логических операций")

    # Арифметические операции с фильтром
    print("=== АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ ===")

    # Попробуем разные значения V для демонстрации
    test_values = [[1, 0, 1], [0, 1, 1], [1, 1, 0], [0, 0, 1]]

    for target_v in test_values:
        matrix_arith = [row[:] for row in matrix]  # Копия исходной матрицы
        matrix_arith = arithmetic_operation(matrix_arith, target_v)

        # Проверяем, были ли найдены совпадения
        matching_words = find_matching_words(matrix, target_v)
        if matching_words:
            print_matrix(matrix_arith, f"Матрица после арифметических операций с V={target_v}")
            break

    # Поиск по соответствию
    print("=== ПОИСК ПО СООТВЕТСТВИЮ ===")
    target_pattern = [1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0]
    best_matches, max_matches = pattern_matching_search(matrix, target_pattern)

    print(f"\nЛучшие совпадения (максимум совпадений: {max_matches}):")
    for word_idx, word in best_matches:
        print(f"Слово {word_idx}: {word}")


if __name__ == "__main__":
    main()
