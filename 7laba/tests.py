import unittest
from main import MatrixProcessor


class TestMatrixProcessor(unittest.TestCase):
    def setUp(self):
        self.size = 16
        self.processor = MatrixProcessor(self.size)
        self.test_matrix = [
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
        self.processor.load_matrix(self.test_matrix)

    # Тесты инициализации
    def test_init_default_size(self):
        mp = MatrixProcessor()
        self.assertEqual(len(mp.matrix), 16)
        self.assertEqual(len(mp.matrix[0]), 16)

    def test_init_custom_size(self):
        mp = MatrixProcessor(8)
        self.assertEqual(len(mp.matrix), 8)
        self.assertEqual(len(mp.matrix[0]), 8)

    # Тесты загрузки матрицы
    def test_load_valid_matrix(self):
        new_matrix = [[0] * 16 for _ in range(16)]
        self.processor.load_matrix(new_matrix)
        self.assertEqual(self.processor.matrix, new_matrix)

    def test_load_invalid_row_count(self):
        with self.assertRaises(ValueError):
            self.processor.load_matrix([[0] * 16] * 15)

    def test_load_invalid_col_count(self):
        with self.assertRaises(ValueError):
            self.processor.load_matrix([[0] * 15] * 16)

    # Тесты извлечения последовательностей
    def test_get_row_sequence_full(self):
        seq = self.processor.get_sequence(0, 0, 'row')
        self.assertEqual(seq, self.test_matrix[0])

    def test_get_row_sequence_partial(self):
        seq = self.processor.get_sequence(0, 10, 'row')
        self.assertEqual(seq, self.test_matrix[0][10:])

    def test_get_col_sequence_full(self):
        seq = self.processor.get_sequence(0, 0, 'col')
        expected = [row[0] for row in self.test_matrix]
        self.assertEqual(seq, expected)

    def test_get_col_sequence_partial(self):
        seq = self.processor.get_sequence(10, 0, 'col')
        expected = [row[0] for row in self.test_matrix[10:]]
        self.assertEqual(seq, expected)

    def test_get_diag_sequence_full(self):
        seq = self.processor.get_sequence(0, 0, 'diag')
        expected = [self.test_matrix[i][i] for i in range(16)]
        self.assertEqual(seq, expected)

    def test_get_diag_sequence_partial(self):
        seq = self.processor.get_sequence(10, 10, 'diag')
        expected = [self.test_matrix[i][i] for i in range(10, 16)]
        self.assertEqual(seq, expected)

    def test_get_sequence_invalid_direction(self):
        with self.assertRaises(ValueError):
            self.processor.get_sequence(0, 0, 'invalid')

    # Тесты работы со столбцами
    def test_get_valid_column(self):
        col = self.processor.get_column(0)
        expected = [row[0] for row in self.test_matrix]
        self.assertEqual(col, expected)

    def test_get_column_invalid_index(self):
        with self.assertRaises(ValueError):
            self.processor.get_column(-1)
        with self.assertRaises(ValueError):
            self.processor.get_column(16)

    # Тесты операций над столбцами
    def test_apply_operation_f0(self):
        self.processor.apply_operation("f0", None, 0)
        self.assertEqual(self.processor.get_column(0), [0] * 16)

    def test_apply_operation_f5(self):
        src_col = self.processor.get_column(1)
        self.processor.apply_operation("f5", 1, 2)
        self.assertEqual(self.processor.get_column(2), src_col)

    def test_apply_operation_f10(self):
        src_col = self.processor.get_column(1)
        expected = [1 - x for x in src_col]
        self.processor.apply_operation("f10", 1, 2)
        self.assertEqual(self.processor.get_column(2), expected)

    def test_apply_operation_f15(self):
        self.processor.apply_operation("f15", None, 0)
        self.assertEqual(self.processor.get_column(0), [1] * 16)

    def test_apply_operation_invalid_op(self):
        with self.assertRaises(ValueError):
            self.processor.apply_operation("invalid", 0, 1)

    def test_apply_operation_invalid_columns(self):
        with self.assertRaises(ValueError):
            self.processor.apply_operation("f5", -1, 0)
        with self.assertRaises(ValueError):
            self.processor.apply_operation("f5", 16, 0)
        with self.assertRaises(ValueError):
            self.processor.apply_operation("f5", 0, -1)
        with self.assertRaises(ValueError):
            self.processor.apply_operation("f5", 0, 16)

    # Тесты сложения полей
    def test_add_fields_valid(self):
        results = self.processor.add_fields(8, 9, [1, 0, 1], 4)
        self.assertTrue(isinstance(results, list))
        for res in results:
            self.assertEqual(len(res), 5)  # (col, pattern, a, b, sum)

    def test_add_fields_no_match(self):
        results = self.processor.add_fields(8, 9, [0, 0, 0], 4)
        self.assertEqual(results, [])

    def test_add_fields_invalid_pattern(self):
        with self.assertRaises(ValueError):
            self.processor.add_fields(0, 1, [1, 0], 4)

    def test_add_fields_invalid_columns(self):
        with self.assertRaises(IndexError):
            self.processor.add_fields(-1, 1, [1, 0, 1], 4)
        with self.assertRaises(IndexError):
            self.processor.add_fields(16, 1, [1, 0, 1], 4)

    # Тесты поиска по шаблону
    def test_search_by_pattern_full_match(self):
        pattern = self.processor.get_column(0)
        matches = self.processor.search_by_pattern(pattern)
        self.assertIn(0, matches)

    def test_search_by_pattern_partial_match(self):
        pattern = [1, 0, 1] + [None] * 13
        matches = self.processor.search_by_pattern(pattern)
        self.assertTrue(len(matches) > 0)
        for col in matches:
            col_data = self.processor.get_column(col)
            self.assertEqual(col_data[:3], [1, 0, 1])

    def test_search_by_pattern_all_none(self):
        matches = self.processor.search_by_pattern([None] * 16)
        self.assertEqual(len(matches), 16)

    def test_search_by_pattern_invalid_length(self):
        with self.assertRaises(ValueError):
            self.processor.search_by_pattern([1] * 15)

    # Тесты поиска наилучшего совпадения
    def test_search_best_match_full(self):
        pattern = self.processor.get_column(0)
        matches, count = self.processor.search_best_match(pattern)
        self.assertEqual(count, 16)
        self.assertTrue(any(col == 0 for col, _ in matches))

    def test_search_best_match_partial(self):
        pattern = [1, 0, 1] + [0] * 13
        matches, count = self.processor.search_best_match(pattern)
        self.assertTrue(count >= 3)
        self.assertTrue(len(matches) > 0)

    def test_search_best_match_none(self):
        pattern = [0] * 16
        matches, count = self.processor.search_best_match(pattern)
        self.assertTrue(count >= 0)

    def test_search_best_match_invalid_length(self):
        with self.assertRaises(ValueError):
            self.processor.search_best_match([1] * 15)

    # Тесты вывода
    def test_print_matrix(self):
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.processor.print_matrix()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn("Матрица:", output)
        self.assertIn("[1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]", output)

    # Тесты граничных случаев
    def test_edge_case_last_element(self):
        # Последний элемент строки
        seq = self.processor.get_sequence(15, 15, 'row')
        self.assertEqual(seq, [0])

        # Последний элемент столбца
        seq = self.processor.get_sequence(15, 15, 'col')
        self.assertEqual(seq, [0])

        # Последний элемент диагонали
        seq = self.processor.get_sequence(15, 15, 'diag')
        self.assertEqual(seq, [0])

    def test_edge_case_empty_sequence(self):
        # За границами строки
        seq = self.processor.get_sequence(0, 16, 'row')
        self.assertEqual(seq, [])

        # За границами столбца
        seq = self.processor.get_sequence(16, 0, 'col')
        self.assertEqual(seq, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)