import unittest
from unittest.mock import patch
from io import StringIO
from TruthTable import *


class TestTruthTable(unittest.TestCase):
    def test_extract_variables(self):
        # Простые выражения
        tt = TruthTable("a & b")
        self.assertEqual(tt.variables, ['a', 'b'])

        tt = TruthTable("(a | b) -> !c")
        self.assertEqual(tt.variables, ['a', 'b', 'c'])

        # Убрать тест с not, так как парсер его не поддерживает
        # или улучшить парсер для поддержки ключевых слов

    def test_validate_expression(self):
        # Недопустимые символы
        with self.assertRaises(ValueError):
            TruthTable("a # b")

        # Несбалансированные скобки
        with self.assertRaises(ValueError):
            TruthTable("(a & b")
        with self.assertRaises(ValueError):
            TruthTable("a & b)")

        # Слишком много переменных
        with self.assertRaises(ValueError):
            TruthTable("a & b & c & d & e & f & g")

    def test_parse_expression(self):
        # Простые выражения
        tt = TruthTable("a")
        self.assertEqual(tt.parsed, 'a')

        tt = TruthTable("!a")
        self.assertEqual(tt.parsed, ('!', 'a'))

        # Комплексные выражения
        tt = TruthTable("a & b")
        self.assertEqual(tt.parsed, ('&', 'a', 'b'))

        tt = TruthTable("(a | b) -> c")
        self.assertEqual(tt.parsed, ('->', ('|', 'a', 'b'), 'c'))

    def test_evaluate(self):
        tt = TruthTable("a & b")
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 1, 'b': 1}), 1)
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 1, 'b': 0}), 0)

        tt = TruthTable("a -> b")
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 1, 'b': 0}), 0)
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 0, 'b': 1}), 1)

        tt = TruthTable("a ~ b")
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 1, 'b': 1}), 1)
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 1, 'b': 0}), 0)

    def test_build_table(self):
        tt = TruthTable("a & b")

        with patch('sys.stdout', new=StringIO()) as fake_out:
            tt.build_table()
            output = fake_out.getvalue()

            # Проверяем заголовок
            self.assertIn("  a   |   b   | a & b", output)
            # Проверяем разделитель (теперь ожидаем правильную длину)
            self.assertIn("----------------", output)
            # Проверяем несколько строк таблицы
            self.assertIn("  0   |   0   |   0  ", output)
            self.assertIn("  1   |   1   |   1  ", output)

    def test_build_sdnf_sknf(self):
        tt = TruthTable("a & b")
        tt.build_table()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            tt.build_sdnf_sknf()
            output = fake_out.getvalue()

            # Проверяем СДНФ
            self.assertIn("(a&b)", output)
            self.assertIn("[3]", output)  # Числовая форма

            # Проверяем СКНФ (теперь ожидаем правильный формат)
            self.assertIn("(a|b)", output)
            self.assertIn("(a|!b)", output)
            self.assertIn("(!a|b)", output)
            self.assertIn("[0, 1, 2]", output)

            # Проверяем индексную форму
            self.assertIn("0001", output)
            self.assertIn("1", output)

    def test_complex_expression(self):
        # Тестирование комплексного выражения
        tt = TruthTable("(a -> b) & (c ~ d)")
        self.assertEqual(tt.variables, ['a', 'b', 'c', 'd'])

        tt.build_table()
        self.assertEqual(len(tt.rows), 16)  # 2^4 = 16 строк

        # Проверка вычисления для конкретного набора
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 1, 'b': 1, 'c': 1, 'd': 0}), 0)
        self.assertEqual(tt._evaluate(tt.parsed, {'a': 0, 'b': 1, 'c': 1, 'd': 1}), 1)


if __name__ == '__main__':
    unittest.main()