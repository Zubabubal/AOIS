class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size  # Хеш-таблица: [ключ, значение, V, h(V)]
        self.count = 0  # Количество заполненных ячеек

    def _calculate_v(self, key):
        """Вычисление числового значения V для ключа (сумма ASCII кодов)"""
        if not isinstance(key, str):
            key = str(key)
        return sum(ord(char) for char in key)

    def _hash_function(self, v):
        """Вычисление хеш-адреса h(V)"""
        return v % self.size

    def _find_slot(self, key, v, h):
        """Поиск свободной ячейки с линейным пробированием"""
        original_h = h
        while self.table[h] is not None:
            # Если ключ уже существует, вернуть его позицию
            if self.table[h][0] == key:
                return h, True
            h = (h + 1) % self.size  # Линейное пробирование
            if h == original_h:  # Полный цикл - таблица полна
                return None, False
        return h, False

    def insert(self, key, value):
        """Вставка новой записи в хеш-таблицу"""
        # Проверка на дубликат ключа
        v = self._calculate_v(key)
        h = self._hash_function(v)
        slot, exists = self._find_slot(key, v, h)

        if exists:
            print(f"Ошибка: Ключ '{key}' уже существует в таблице!")
            return False

        if slot is None:
            print("Ошибка: Хеш-таблица заполнена!")
            return False

        # Вставка новой записи
        self.table[slot] = [key, value, v, h]
        self.count += 1
        print(f"Запись добавлена: ключ='{key}', значение='{value}', V={v}, h(V)={h}, позиция={slot}")
        return True

    def search(self, key):
        """Поиск записи по ключу"""
        v = self._calculate_v(key)
        h = self._hash_function(v)
        original_h = h

        while self.table[h] is not None:
            if self.table[h][0] == key:
                return self.table[h]
            h = (h + 1) % self.size
            if h == original_h:
                break
        print(f"Ключ '{key}' не найден в таблице!")
        return None

    def delete(self, key):
        """Удаление записи по ключу"""
        v = self._calculate_v(key)
        h = self._hash_function(v)
        original_h = h

        while self.table[h] is not None:
            if self.table[h][0] == key:
                self.table[h] = None
                self.count -= 1
                print(f"Запись с ключом '{key}' удалена из позиции {h}")
                return True
            h = (h + 1) % self.size
            if h == original_h:
                break
        print(f"Ключ '{key}' не найден для удаления!")
        return False

    def get_fill_factor(self):
        """Расчет коэффициента заполнения"""
        return self.count / self.size

    def display(self):
        """Вывод содержимого хеш-таблицы"""
        print("\nСодержимое хеш-таблицы:")
        print(f"{'Индекс':<8} {'Ключ':<15} {'Значение':<15} {'V':<8} {'h(V)':<8}")
        print("-" * 54)
        for i in range(self.size):
            if self.table[i] is not None:
                key, value, v, h = self.table[i]
                print(f"{i:<8} {key:<15} {value:<15} {v:<8} {h:<8}")
            else:
                print(f"{i:<8} {'-':<15} {'-':<15} {'-':<8} {'-':<8}")
        print(f"\nКоэффициент заполнения: {self.get_fill_factor():.2f}\n")

