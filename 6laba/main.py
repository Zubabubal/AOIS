from hash_table import HashTable

# Пример использования
if __name__ == "__main__":
    ht = HashTable(size=10)

    # Вставка записей
    ht.insert("apple", "fruit")
    ht.insert("banana", "fruit")
    ht.insert("carrot", "vegetable")
    ht.insert("dog", "animal")

    # Попытка вставить дубликат
    ht.insert("apple", "new_fruit")

    # Вывод таблицы
    ht.display()

    # Поиск
    result = ht.search("banana")
    if result:
        print(f"Найдена запись: {result}")

    # Удаление
    ht.delete("carrot")

    # Вывод таблицы после удаления
    ht.display()

    # Поиск несуществующего ключа
    ht.search("orange")