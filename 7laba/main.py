class MatrixProcessor:
    def __init__(self, size=16):
        self.size = size
        self.matrix = [[0] * size for _ in range(size)]

    def print_matrix(self, title="Матрица:"):
        print(title)
        for row in self.matrix:  # Нормальный порядок строк
            print(f"[{', '.join(map(str, row))}]")
        print()

    def load_matrix(self, matrix):
        if len(matrix) == self.size and all(len(row) == self.size for row in matrix):
            self.matrix = [row[:] for row in matrix]
        else:
            raise ValueError("Неверный размер матрицы")

    def get_sequence(self, start_row, start_col, direction='row'):
        sequence = []
        if direction == 'row':
            sequence = self.matrix[start_row][start_col:self.size]
        elif direction == 'col':
            sequence = [self.matrix[row][start_col] for row in range(start_row, self.size)]
        elif direction == 'diag':
            row, col = start_row, start_col
            while row < self.size and col < self.size:
                sequence.append(self.matrix[row][col])
                row += 1
                col += 1
        return sequence

    def get_column(self, col_index):
        if col_index < 0 or col_index >= self.size:
            raise ValueError("Неверный индекс столбца")
        return [self.matrix[row][col_index] for row in range(self.size)]

    def apply_operation(self, op, src_col, dst_col):
        if src_col is not None and not (0 <= src_col < self.size):
            raise ValueError("Неверный исходный столбец")
        if not (0 <= dst_col < self.size):
            raise ValueError("Неверный целевой столбец")
        for row in range(self.size):
            if op == "f0":
                self.matrix[row][dst_col] = 0
            elif op == "f5" and src_col is not None:
                self.matrix[row][dst_col] = self.matrix[row][src_col]
            elif op == "f10" and src_col is not None:
                self.matrix[row][dst_col] = 1 - self.matrix[row][src_col]
            elif op == "f15":
                self.matrix[row][dst_col] = 1
        op_name = 'копирования' if op in ['f0', 'f5'] else 'инверсии' if op == 'f10' else 'заполнения 1'
        src_text = f"от столбца {src_col} к {dst_col}" if src_col is not None else f"к столбцу {dst_col}"
        print(f"Применение операции {op_name} ({op}) {src_text}:")
        print(f"Результат (столбец {dst_col}):")
        print(self.get_column(dst_col))
        self.print_matrix()

    def add_fields(self, a_col, b_col, v_pattern, field_size=4):
        if len(v_pattern) != 3:
            raise ValueError("Длина V-образного шаблона должна быть 3")
        results = []
        for col in range(self.size):
            if all(self.matrix[row][col] == v_pattern[row] for row in range(3)):
                a_val = [self.matrix[i][a_col] for i in range(3, 3 + field_size)]
                b_val = [self.matrix[i][b_col] for i in range(3, 3 + field_size)]
                a_num = int(''.join(map(str, a_val)), 2)
                b_num = int(''.join(map(str, b_val)), 2)
                sum_val = a_num + b_num
                sum_bits = [int(bit) for bit in format(sum_val, f'0{field_size+1}b')[-field_size-1:]]
                results.append((col, v_pattern, a_val, b_val, sum_bits))
                for i in range(min(len(sum_bits), 5)):
                    self.matrix[i][col] = sum_bits[i]
        return results

    def search_by_pattern(self, pattern):
        if len(pattern) != self.size:
            raise ValueError("Длина шаблона должна соответствовать размеру матрицы")
        results = []
        for col in range(self.size):
            match = all(pattern[row] is None or self.matrix[row][col] == pattern[row] for row in range(self.size))
            if match:
                results.append(col)
        return results

    def search_best_match(self, pattern):
        if len(pattern) != self.size:
            raise ValueError("Длина шаблона должна соответствовать размеру матрицы")
        max_matches = 0
        best_matches = []
        for col in range(self.size):
            matches = sum(1 for row in range(self.size) if self.matrix[row][col] == pattern[row])
            if matches > max_matches:
                max_matches = matches
                best_matches = [(col, self.get_column(col))]
            elif matches == max_matches:
                best_matches.append((col, self.get_column(col)))
        return best_matches, max_matches


if __name__ == "__main__":
    processor = MatrixProcessor(16)
    test_matrix = [
        [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0]
    ]
    processor.load_matrix(test_matrix)
    processor.print_matrix("Исходная матрица:")

    print("Извлечение последовательности 0 (начиная с позиции (0,0)):")
    seq0 = processor.get_sequence(0, 0, 'row')
    print("Последовательность 0:")
    print(seq0)
    print()

    print("Извлечение последовательности 1 (начиная с позиции (1,1)):")
    seq1 = processor.get_sequence(1, 1, 'row')
    print("Последовательность 1:")
    print(seq1)
    print()

    print("Извлечение диагональной последовательности 3 (начиная с позиции (3,0)):")
    seq_diag = processor.get_sequence(3, 0, 'diag')
    print("Диагональная последовательность 3:")
    print(seq_diag)
    print()

    processor.apply_operation("f0", 0, 2)
    processor.apply_operation("f5", 1, 3)
    processor.apply_operation("f10", 1, 4)
    processor.apply_operation("f15", None, 5)

    print("Поиск столбцов, где первые 3 бита [1, 0, 1]:")
    pattern = [1, 0, 1] + [None] * 13
    matching_cols = processor.search_by_pattern(pattern)
    print("Найденные столбцы:")
    for col in matching_cols:
        print(f"Столбец {col}: {processor.get_column(col)[:3]}")
    print()

    print("Обработка полей с фильтром [1, 0, 1]:")
    v_pattern = [1, 0, 1]
    sums = processor.add_fields(8, 9, v_pattern, 4)
    print("Обновленные записи (индекс столбца, новое слово):")
    for col, p, a, b, s in sums:
        print(f"Столбец {col}: P={p}, A={a}, B={b}, S={s}")
    processor.print_matrix()

    print("Поиск лучшего совпадения с образцом [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1]:")
    pattern = [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1]
    matches, max_matches = processor.search_best_match(pattern)
    print("Лучшие совпадения (индекс столбца, слово):")
    for col, word in matches:
        print(f"Столбец {col}: {word}")
    print(f"Максимальное число совпадений: {max_matches}")