from truthtable import TruthTable

def main():
    print("=== ПОСТРОЕНИЕ ТАБЛИЦЫ ИСТИННОСТИ ===")
    print("Выберите вариант:")
    print("1. Использовать готовые сложные примеры")
    print("2. Ввести свое логическое выражение")
    print("3. Протестировать все примеры автоматически")

    choice = input("Ваш выбор (1/2/3): ")

    if choice == "1":
        examples = [
            ("(!((a&b)|(!(c->(d~e)))))", "Сложное вложенное выражение с 5 переменными"),
            ("((a|(b&c))~((d->e)&(!f)))", "Комплексное выражение с 6 переменными"),
            ("(((!a)|(b&c))->(d~(e&f)))", "Импликация с комплексными условиями"),
            ("(((a->b)&(c~d))|(!(e&f)))", "Комбинация операторов с разными приоритетами"),
            ("(!(a&(b|(c&(d->(e~f))))))", "Глубокая вложенность операторов"),
            ("((a~b)&(c|!d)->(e&f))", "Комбинированное выражение с импликацией"),
            ("(!a|(b&(c~(d->e))))", "Отрицание с комплексными условиями"),
            ("((a&b)|(!(c->(d~e)))->f)", "Многоуровневая логическая конструкция")
        ]

        print("\nДоступные сложные примеры:")
        for i, (expr, desc) in enumerate(examples, 1):
            print(f"{i}. {expr} - {desc}")

        example_choice = int(input("Выберите номер примера (1-8): ")) - 1
        if 0 <= example_choice < len(examples):
            expr = examples[example_choice][0]
        else:
            print("Неверный номер примера")
            return

    elif choice == "2":
        expr = input("Введите сложное логическое выражение (можно использовать: &, |, !, ->, ~, скобки): ")
        print("\nПроверяем выражение:", expr)
    elif choice == "3":
        print("\nЗапуск автоматического тестирования всех сложных примеров...")
        test_all_examples()
        return
    else:
        print("Неверный выбор")
        return

    try:
        print("\nАнализ выражения:", expr)
        tt = TruthTable(expr)
        print(f"Обнаружены переменные: {', '.join(tt.variables)}")
        print(f"Общее количество комбинаций: {2 ** len(tt.variables)}")

        tt.build_table()
        tt.build_sdnf_sknf()

        print("\nДополнительная информация:")
        print(f"Количество единиц в функции: {sum(row[-1] for row in tt.rows)}")
        print(f"Количество нулей в функции: {len(tt.rows) - sum(row[-1] for row in tt.rows)}")

    except ValueError as e:
        print(f"\nОшибка в выражении: {e}")
    except Exception as e:
        print(f"\nНеожиданная ошибка: {e}")


def test_all_examples():
    test_cases = [
        ("(!((a&b)|(!(c->(d~e)))))", True),
        ("((a|(b&c))~((d->e)&(!f)))", True),
        ("(((!a)|(b&c))->(d~(e&f)))", True),
        ("(((a->b)&(c~d))|(!(e&f)))", True),
        ("(!(a&(b|(c&(d->(e~f))))))", True),
        ("((a~b)&(c|!d)->(e&f))", True),
        ("(!a|(b&(c~(d->e))))", True),
        ("((a&b)|(!(c->(d~e)))->f)", True),
        ("(a&b&c&d&e&f)", True),  # Все единицы
        ("(a|b|c|d|e|f)", True)  # Все нули кроме последнего
    ]

    for expr, expected in test_cases:
        print(f"\n\n=== ТЕСТИРУЕМ ВЫРАЖЕНИЕ: {expr} ===")
        try:
            tt = TruthTable(expr)
            print(f"Переменные: {tt.variables}")
            tt.build_table()
            tt.build_sdnf_sknf()

            # Проверка минимального/максимального количества переменных
            if len(tt.variables) < 3:
                print("Предупреждение: пример слишком простой, рекомендуется использовать более сложные выражения")

        except Exception as e:
            print(f"Ошибка при тестировании: {e}")
            if expected:
                print("!!! Этот тест должен был пройти успешно !!!")


if __name__ == "__main__":
    main()
