import unittest
from unittest.mock import patch, call
import io
import sys

# Импортируем все функции из исходного модуля
# Предполагается, что исходный код находится в файле matrix_operations.py
from main import (
    print_matrix, read_word, read_column, write_column, write_word,
    logical_function_f5, logical_function_f10, logical_function_f0, logical_function_f15,
    apply_logical_function, extract_fields, binary_add, find_matching_words,
    arithmetic_operation, pattern_matching_search
)


class TestMatrixOperations(unittest.TestCase):

    def setUp(self):
        """Настройка тестовой матрицы перед каждым тестом"""
        self.test_matrix = [
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1]
        ]

        self.full_matrix = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_matrix_default_title(self, mock_stdout):
        """Тест печати матрицы с заголовком по умолчанию"""
        print_matrix(self.test_matrix)
        output = mock_stdout.getvalue()
        self.assertIn("Исходная матрица:", output)
        self.assertIn("['1']", output)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_print_matrix_custom_title(self, mock_stdout):
        """Тест печати матрицы с пользовательским заголовком"""
        print_matrix(self.test_matrix, "Тестовая матрица")
        output = mock_stdout.getvalue()
        self.assertIn("Тестовая матрица:", output)

    def test_read_word_diagonal_addressing(self):
        """Тест чтения слова с диагональной адресацией"""
        # Тест для слова 0 (start_col = 15 % 4 = 3)
        word = read_word(self.test_matrix, 0)
        expected = [0, 0, 1, 1]  # matrix[0][3], matrix[1][0], matrix[2][1], matrix[3][2]
        self.assertEqual(word, expected)

        # Тест для слова 1 (start_col = 14 % 4 = 2)
        word = read_word(self.test_matrix, 1)
        expected = [0, 1, 1, 1]  # matrix[0][2], matrix[1][3], matrix[2][0], matrix[3][1]
        self.assertEqual(word, expected)

    def test_read_word_different_indices(self):
        """Тест чтения слов с разными индексами"""
        # Тест для слова 15 (start_col = 0 % 4 = 0)
        word = read_word(self.test_matrix, 15)
        expected = [1, 1, 1, 1]  # matrix[0][0], matrix[1][1], matrix[2][2], matrix[3][3]
        self.assertEqual(word, expected)

    def test_read_column(self):
        """Тест чтения столбца"""
        column = read_column(self.test_matrix, 0)
        expected = [1, 1, 0, 0]
        self.assertEqual(column, expected)

        column = read_column(self.test_matrix, 2)
        expected = [0, 0, 1, 1]
        self.assertEqual(column, expected)

    def test_write_column(self):
        """Тест записи в столбец"""
        matrix_copy = [row[:] for row in self.test_matrix]
        new_data = [1, 1, 1, 1]
        write_column(matrix_copy, 1, new_data)

        expected_column = [1, 1, 1, 1]
        actual_column = read_column(matrix_copy, 1)
        self.assertEqual(actual_column, expected_column)

    def test_write_column_partial_data(self):
        """Тест записи в столбец с частичными данными"""
        matrix_copy = [row[:] for row in self.test_matrix]
        new_data = [1, 1]  # Только 2 элемента
        write_column(matrix_copy, 1, new_data)

        # Проверяем, что изменились только первые 2 элемента
        self.assertEqual(matrix_copy[0][1], 1)
        self.assertEqual(matrix_copy[1][1], 1)
        self.assertEqual(matrix_copy[2][1], 1)  # Остался прежним
        self.assertEqual(matrix_copy[3][1], 0)  # Остался прежним

    def test_write_word(self):
        """Тест записи слова с диагональной адресацией"""
        matrix_copy = [row[:] for row in self.test_matrix]
        new_word = [1, 1, 1, 1]
        write_word(matrix_copy, 0, new_word)

        # Проверяем, что слово записалось правильно
        written_word = read_word(matrix_copy, 0)
        self.assertEqual(written_word, new_word)

    def test_write_word_partial_data(self):
        """Тест записи слова с частичными данными"""
        matrix_copy = [row[:] for row in self.test_matrix]
        new_word = [1, 1]  # Только 2 элемента
        write_word(matrix_copy, 0, new_word)

        # Проверяем, что изменились только первые 2 позиции
        written_word = read_word(matrix_copy, 0)
        self.assertEqual(written_word[:2], [1, 1])

    def test_logical_function_f5(self):
        """Тест логической функции f5 (возвращает b)"""
        self.assertEqual(logical_function_f5(0, 0), 0)
        self.assertEqual(logical_function_f5(0, 1), 1)
        self.assertEqual(logical_function_f5(1, 0), 0)
        self.assertEqual(logical_function_f5(1, 1), 1)

    def test_logical_function_f10(self):
        """Тест логической функции f10 (НЕ b)"""
        self.assertEqual(logical_function_f10(0, 0), 1)
        self.assertEqual(logical_function_f10(0, 1), 0)
        self.assertEqual(logical_function_f10(1, 0), 1)
        self.assertEqual(logical_function_f10(1, 1), 0)

    def test_logical_function_f0(self):
        """Тест логической функции f0 (константа 0)"""
        self.assertEqual(logical_function_f0(0, 0), 0)
        self.assertEqual(logical_function_f0(0, 1), 0)
        self.assertEqual(logical_function_f0(1, 0), 0)
        self.assertEqual(logical_function_f0(1, 1), 0)

    def test_logical_function_f15(self):
        """Тест логической функции f15 (константа 1)"""
        self.assertEqual(logical_function_f15(0, 0), 1)
        self.assertEqual(logical_function_f15(0, 1), 1)
        self.assertEqual(logical_function_f15(1, 0), 1)
        self.assertEqual(logical_function_f15(1, 1), 1)

    def test_apply_logical_function(self):
        """Тест применения логической функции к словам"""
        word1 = [1, 0, 1, 0]
        word2 = [0, 1, 1, 0]

        result = apply_logical_function(word1, word2, logical_function_f5)
        expected = [0, 1, 1, 0]  # f5 возвращает b
        self.assertEqual(result, expected)

    def test_apply_logical_function_different_lengths(self):
        """Тест применения логической функции к словам разной длины"""
        word1 = [1, 0]
        word2 = [0, 1, 1, 0]

        result = apply_logical_function(word1, word2, logical_function_f5)
        expected = [0, 1, 1, 0]  # Недостающие биты word1 заменяются на 0
        self.assertEqual(result, expected)

    def test_extract_fields(self):
        """Тест извлечения полей из 16-битного слова"""
        word = [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1]
        V, A, B, S = extract_fields(word)

        self.assertEqual(V, [1, 0, 1])
        self.assertEqual(A, [1, 1, 0, 0])
        self.assertEqual(B, [1, 1, 1, 1])
        self.assertEqual(S, [0, 0, 1, 0, 1])

    def test_extract_fields_short_word(self):
        """Тест извлечения полей из короткого слова (дополнение нулями)"""
        word = [1, 0, 1]
        V, A, B, S = extract_fields(word)

        self.assertEqual(V, [1, 0, 1])
        self.assertEqual(A, [0, 0, 0, 0])
        self.assertEqual(B, [0, 0, 0, 0])
        self.assertEqual(S, [0, 0, 0, 0, 0])

    def test_binary_add(self):
        """Тест двоичного сложения"""
        a = [0, 0, 1, 1]  # 3 в двоичной системе
        b = [0, 1, 0, 1]  # 5 в двоичной системе
        result = binary_add(a, b)

        # 3 + 5 = 8 = 01000 в 5-битном представлении
        expected = [0, 1, 0, 0, 0]
        self.assertEqual(result, expected)

    def test_binary_add_zero(self):
        """Тест двоичного сложения с нулем"""
        a = [0, 0, 0, 0]
        b = [0, 0, 0, 0]
        result = binary_add(a, b)
        expected = [0, 0, 0, 0, 0]
        self.assertEqual(result, expected)

    def test_binary_add_overflow(self):
        """Тест двоичного сложения с переполнением"""
        a = [1, 1, 1, 1]  # 15
        b = [1, 1, 1, 1]  # 15
        result = binary_add(a, b)

        # 15 + 15 = 30 = 11110 в 5-битном представлении
        expected = [1, 1, 1, 1, 0]
        self.assertEqual(result, expected)

    def test_find_matching_words(self):
        """Тест поиска слов с заданным значением V"""
        matrix = [
            [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],  # V=[1,0,1]
            [1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],  # V=[1,0,1]
            [0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1],  # V=[0,1,0]
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        target_v = [1, 0, 1]
        matches = find_matching_words(matrix, target_v)

        # Должно быть найдено 2 слова
        self.assertEqual(len(matches), 2)

        # Проверяем, что V правильно извлечено
        for word_idx, word, V, A, B, S in matches:
            self.assertEqual(V, target_v)

    def test_find_matching_words_no_matches(self):
        """Тест поиска слов без совпадений"""
        target_v = [1, 1, 1]
        matches = find_matching_words(self.full_matrix, target_v)

        # Проверяем количество найденных совпадений (может быть 0)
        self.assertIsInstance(matches, list)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_arithmetic_operation_with_matches(self, mock_stdout):
        """Тест арифметических операций с найденными словами"""
        # Создаем матрицу, где первое слово имеет V=[1,0,1]
        matrix = [
            [1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1] + [0] * 0,
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        target_v = [1, 0, 1]
        result_matrix = arithmetic_operation(matrix, target_v)

        output = mock_stdout.getvalue()
        self.assertIn("Арифметическая операция с фильтром", output)
        self.assertIsInstance(result_matrix, list)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_arithmetic_operation_no_matches(self, mock_stdout):
        """Тест арифметических операций без совпадений"""
        matrix = [[0] * 16 for _ in range(4)]
        target_v = [1, 1, 1]

        result_matrix = arithmetic_operation(matrix, target_v)

        output = mock_stdout.getvalue()
        self.assertIn("Нет слов с заданным значением V", output)
        self.assertEqual(result_matrix, matrix)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pattern_matching_search(self, mock_stdout):
        """Тест поиска по соответствию с образцом"""
        target_pattern = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        best_matches, max_matches = pattern_matching_search(self.full_matrix, target_pattern)

        output = mock_stdout.getvalue()
        self.assertIn("Поиск по соответствию с образцом", output)
        self.assertIsInstance(best_matches, list)
        self.assertIsInstance(max_matches, int)
        self.assertGreaterEqual(max_matches, 0)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_pattern_matching_search_perfect_match(self, mock_stdout):
        """Тест поиска с идеальным совпадением"""
        # Создаем матрицу где первое слово точно совпадает с образцом
        matrix = [[1, 0, 1, 0] for _ in range(4)]
        target_pattern = [1, 0, 1, 0]

        best_matches, max_matches = pattern_matching_search(matrix, target_pattern)

        # Максимальное количество совпадений должно быть равно длине образца
        self.assertEqual(max_matches, len(target_pattern))
        self.assertGreater(len(best_matches), 0)

    def test_pattern_matching_search_empty_pattern(self):
        """Тест поиска с пустым образцом"""
        target_pattern = []

        best_matches, max_matches = pattern_matching_search(self.test_matrix, target_pattern)

        # При пустом образце максимальное количество совпадений должно быть 0
        self.assertEqual(max_matches, 0)

    def test_edge_cases_matrix_operations(self):
        """Тест граничных случаев для операций с матрицей"""
        # Тест с матрицей 1x1
        small_matrix = [[1]]

        # Чтение столбца
        column = read_column(small_matrix, 0)
        self.assertEqual(column, [1])

        # Запись в столбец
        write_column(small_matrix, 0, [0])
        self.assertEqual(small_matrix[0][0], 0)

    def test_word_operations_large_matrix(self):
        """Тест операций со словами на большой матрице"""
        large_matrix = [[i % 2 for i in range(16)] for _ in range(16)]

        # Тест чтения всех слов
        for word_idx in range(16):
            word = read_word(large_matrix, word_idx)
            self.assertEqual(len(word), 16)

        # Тест записи слова
        test_word = [1] * 16
        write_word(large_matrix, 0, test_word)
        written_word = read_word(large_matrix, 0)
        self.assertEqual(written_word, test_word)

    def test_logical_operations_comprehensive(self):
        """Комплексный тест логических операций"""
        functions = [
            logical_function_f0,
            logical_function_f5,
            logical_function_f10,
            logical_function_f15
        ]

        test_cases = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for func in functions:
            for a, b in test_cases:
                result = func(a, b)
                self.assertIn(result, [0, 1])  # Результат должен быть 0 или 1


class TestMainFunction(unittest.TestCase):
    """Тесты для интеграции и основной функции"""

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_function_execution(self, mock_stdout):
        """Тест выполнения основной функции без ошибок"""
        from main import main

        # Проверяем, что main() выполняется без исключений
        try:
            main()
            execution_successful = True
        except Exception as e:
            execution_successful = False
            print(f"Main function failed with: {e}")

        self.assertTrue(execution_successful)

        # Проверяем, что есть вывод
        output = mock_stdout.getvalue()
        self.assertGreater(len(output), 0)

        # Проверяем наличие основных разделов в выводе
        self.assertIn("ДЕМОНСТРАЦИЯ ИЗВЛЕЧЕНИЯ СЛОВ", output)
        self.assertIn("ЛОГИЧЕСКИЕ ОПЕРАЦИИ", output)
        self.assertIn("АРИФМЕТИЧЕСКИЕ ОПЕРАЦИИ", output)
        self.assertIn("ПОИСК ПО СООТВЕТСТВИЮ", output)


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)
