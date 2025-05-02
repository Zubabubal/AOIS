import unittest
from Karno import TruthTable


class TestTruthTable(unittest.TestCase):

    def test_valid_initialization(self):
        print("\nТест 1: Проверка инициализации с валидными выражениями")
        cases = [
            ("A", ["A"]),
            ("A & B", ["A", "B"]),
            ("A | B -> C", ["A", "B", "C"])
        ]
        for expr, expected_vars in cases:
            with self.subTest(expr=expr):
                print(f"Проверка выражения: {expr}")
                tt = TruthTable(expr)
                self.assertEqual(tt.original_expression, expr)
                self.assertEqual(tt.variables, expected_vars)
                print(f"✓ Успешно: {expr}")

    def test_invalid_expressions(self):
        print("\nТест 2: Проверка обработки невалидных выражений")
        cases = [
            ("", "Пустое выражение"),
            ("A &", "Неполное выражение"),
            ("A $ B", "Недопустимые символы"),
            ("(A & B", "Несбалансированные скобки"),
            ("A & B & C & D & E & F & G", "Слишком много переменных")
        ]
        for expr, desc in cases:
            with self.subTest(desc=desc):
                print(f"Проверка: {desc}")
                with self.assertRaises(ValueError):
                    TruthTable(expr)
                print(f"✓ Успешно: {desc}")

    def test_truth_table_construction(self):
        print("\nТест 3: Проверка построения таблицы истинности")
        test_cases = [
            ("A", 2),
            ("A & B", 4),
            ("A | B | C", 8)
        ]

        for expr, expected_rows in test_cases:
            with self.subTest(expr=expr):
                print(f"Проверка выражения: {expr}")
                tt = TruthTable(expr)
                tt.build_table()
                self.assertEqual(len(tt.rows), expected_rows)
                print(f"✓ Успешно: {expr} - {expected_rows} строк")

    def test_perfect_forms_generation(self):
        print("\nТест 4: Проверка генерации СДНФ/СКНФ")
        test_cases = [
            ("A & B", 1, 3),
            ("A | B", 3, 1),
            ("A", 1, 1)
        ]

        for expr, sdnf_terms, sknf_terms in test_cases:
            with self.subTest(expr=expr):
                print(f"\nПроверка выражения: {expr}")
                tt = TruthTable(expr)
                sdnf, sknf = tt.build_sdnf_sknf()
                print(f"СДНФ: {sdnf}")
                print(f"СКНФ: {sknf}")

                if sdnf != "0":
                    self.assertEqual(len(sdnf.split("|")), sdnf_terms)
                if sknf != "1":
                    self.assertEqual(len(sknf.split("&")), sknf_terms)
                print(f"✓ Успешно: {expr}")

    def test_minimization_methods(self):
        print("\nТест 5: Проверка методов минимизации")
        test_cases = [
            ("(A & B) | (A & !B)", "A"),
            ("A", "A")
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                print(f"\nПроверка выражения: {expr}")
                tt = TruthTable(expr)
                tt.build_sdnf_sknf()
                result = tt.minimize_dnf_calculation()
                print(f"Результат минимизации: {result}")

                if expected == "0":
                    self.assertEqual(result, expected)
                else:
                    self.assertIn(expected, result)
                print(f"✓ Успешно: {expr} -> {expected}")

    def test_3_variable_expression(self):
        print("\nТест 6: Проверка работы с 3 переменными")
        expr = "A & (B | C)"
        print(f"Проверка выражения: {expr}")
        tt = TruthTable(expr)
        tt.build_table()
        self.assertEqual(len(tt.rows), 8)

        for row in tt.rows:
            a, b, c, result = row
            self.assertEqual(result, a and (b or c))
        print("✓ Успешно: корректная работа с 3 переменными")

    def test_edge_cases(self):
        print("\nТест 7: Проверка крайних случаев")

        print("Проверка всегда истинного выражения (A | !A)")
        tt = TruthTable("A | !A")
        sdnf, sknf = tt.build_sdnf_sknf()
        print(f"СДНФ: {sdnf}")
        print(f"СКНФ: {sknf}")
        self.assertNotEqual(sdnf, "0")
        self.assertEqual(sknf, "1")

        print("Проверка всегда ложного выражения (A & !A)")
        tt = TruthTable("A & !A")
        sdnf, sknf = tt.build_sdnf_sknf()
        print(f"СДНФ: {sdnf}")
        print(f"СКНФ: {sknf}")
        self.assertEqual(sdnf, "0")
        self.assertNotEqual(sknf, "1")

        print("✓ Успешно: все крайние случаи обработаны")


if __name__ == '__main__':
    print("Запуск тестов TruthTable\n" + "=" * 50)
    unittest.main(verbosity=2)