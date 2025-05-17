import unittest
from io import StringIO
import sys
from hash_table import HashTable  # Предполагается, что класс HashTable находится в файле hashtable.py

class TestHashTable(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.ht = HashTable(size=5)  # Маленький размер для удобства тестирования

    def test_constructor(self):
        """Тест конструктора: проверка размера и начального состояния."""
        self.assertEqual(self.ht.size, 5)
        self.assertEqual(self.ht.table, [None] * 5)
        self.assertEqual(self.ht.count, 0)

    def test_calculate_v(self):
        """Тест метода _calculate_v для строк и чисел."""
        self.assertEqual(self.ht._calculate_v("a"), ord("a"))
        self.assertEqual(self.ht._calculate_v("ab"), ord("a") + ord("b"))
        self.assertEqual(self.ht._calculate_v(123), sum(ord(char) for char in "123"))
        self.assertEqual(self.ht._calculate_v(""), 0)  # Пустая строка

    def test_hash_function(self):
        """Тест метода _hash_function."""
        self.assertEqual(self.ht._hash_function(0), 0)
        self.assertEqual(self.ht._hash_function(5), 0)  # 5 % 5 = 0
        self.assertEqual(self.ht._hash_function(6), 1)  # 6 % 5 = 1
        self.assertEqual(self.ht._hash_function(-1), 4)  # -1 % 5 = 4

    def test_find_slot(self):
        """Тест метода _find_slot: свободные ячейки, коллизии, полная таблица."""
        # Пустая таблица
        slot, exists = self.ht._find_slot("a", self.ht._calculate_v("a"), 0)
        self.assertEqual(slot, 0)
        self.assertFalse(exists)

        # Вставляем запись
        self.ht.table[0] = ["a", "value_a", self.ht._calculate_v("a"), 0]
        self.ht.count += 1

        # Существующий ключ
        slot, exists = self.ht._find_slot("a", self.ht._calculate_v("a"), 0)
        self.assertEqual(slot, 0)
        self.assertTrue(exists)

        # Коллизия
        v_b = self.ht._calculate_v("b")
        h_b = self.ht._hash_function(v_b)
        if h_b == 0:
            slot, exists = self.ht._find_slot("b", v_b, h_b)
            self.assertEqual(slot, 1)
            self.assertFalse(exists)

        # Полная таблица
        for i in range(1, 5):
            self.ht.table[i] = [f"key{i}", f"value{i}", i, i % 5]
            self.ht.count += 1
        slot, exists = self.ht._find_slot("new", self.ht._calculate_v("new"), 0)
        self.assertIsNone(slot)
        self.assertFalse(exists)


    def test_search(self):
        """Тест метода search: существующий и несуществующий ключ."""
        self.ht.insert("a", "value_a")
        self.ht.insert("b", "value_b")

        # Существующий ключ
        result = self.ht.search("a")
        self.assertEqual(result, ["a", "value_a", self.ht._calculate_v("a"), 2])

        # Несуществующий ключ
        result = self.ht.search("c")
        self.assertIsNone(result)

        # Коллизия
        v_d = self.ht._calculate_v("d")
        h_d = self.ht._hash_function(v_d)
        if h_d == 0:
            self.ht.insert("d", "value_d")
            result = self.ht.search("d")
            self.assertEqual(result, ["d", "value_d", v_d, h_d])

    def test_delete(self):
        """Тест метода delete: существующий и несуществующий ключ."""
        self.ht.insert("a", "value_a")
        self.ht.insert("b", "value_b")

        # Существующий ключ
        self.assertTrue(self.ht.delete("a"))
        self.assertIsNone(self.ht.table[0])
        self.assertEqual(self.ht.count, 1)

        # Несуществующий ключ
        self.assertFalse(self.ht.delete("c"))
        self.assertEqual(self.ht.count, 1)

        # Удаление из таблицы с коллизиями
        v_d = self.ht._calculate_v("d")
        h_d = self.ht._hash_function(v_d)
        if h_d == self.ht._hash_function(self.ht._calculate_v("b")):
            self.ht.insert("d", "value_d")
            self.assertTrue(self.ht.delete("d"))
            self.assertEqual(self.ht.count, 1)

    def test_get_fill_factor(self):
        """Тест метода get_fill_factor: пустая, частичная, полная таблица."""
        self.assertEqual(self.ht.get_fill_factor(), 0.0)

        self.ht.insert("a", "value_a")
        self.assertEqual(self.ht.get_fill_factor(), 1.0 / 5)

        for i in range(1, 5):
            self.ht.insert(f"key{i}", f"value{i}")
        self.assertEqual(self.ht.get_fill_factor(), 1.0)

    def test_display(self):
        """Тест метода display: проверка отсутствия ошибок."""
        self.ht.insert("a", "value_a")
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            self.ht.display()
            self.assertTrue(out.getvalue())  # Проверяем, что есть вывод
        finally:
            sys.stdout = saved_stdout

if __name__ == "__main__":
    unittest.main()