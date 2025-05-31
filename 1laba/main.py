# main.py
from number_operations import NumberOperations


def main():
    no = NumberOperations()

    print("Сложение:")
    print("Ввод числа №1")
    a = int(input())
    print("Число введено:", a)
    direct_a = no.to_direct_code(a)
    ones_a = no.to_inverse_code(a)
    twos_a = no.to_complement_code(a)
    print("Прямой код:", [direct_a])
    print("Обратный код:", [ones_a])
    print("Дополнительный код:", [twos_a])

    print("Ввод числа №2")
    b = int(input())
    print("Число введено:", b)
    direct_b = no.to_direct_code(b)
    ones_b = no.to_inverse_code(b)
    twos_b = no.to_complement_code(b)
    print("Прямой код:", [direct_b])
    print("Обратный код:", [ones_b])
    print("Дополнительный код:", [twos_b])

    print("\nСложение:")
    result_bin = no.add_complement_code(a, b)
    result_dec = no.binary_to_decimal(result_bin)
    print("Результат:", result_dec)

    direct_res = no.to_direct_code(result_dec)
    ones_res = no.to_inverse_code(result_dec)
    twos_res = no.to_complement_code(result_dec)
    print("Прямой код:", [direct_res])
    print("Обратный код:", [ones_res])
    print("Дополнительный код:", [twos_res])

    print("\nВычитание:")
    result_bin = no.subtract_complement_code(a, b)
    result_dec = no.binary_to_decimal(result_bin)
    print("Результат:", result_dec)

    direct_res = no.to_direct_code(result_dec)
    ones_res = no.to_inverse_code(result_dec)
    twos_res = no.to_complement_code(result_dec)
    print("Прямой код:", [direct_res])
    print("Обратный код:", [ones_res])
    print("Дополнительный код:", [twos_res])

    print("\nУмножение:")
    direct_result = ''.join(map(str, no.multiply_direct_code(a, b)))
    result_dec = a * b
    print("Результат в прямом коде:", [direct_result], " Десятичный результат:", result_dec)

    print("\nДеление:")
    bin_result, decimal_result = no.divide_direct_code(a, b)
    print("Результат в прямом коде:", [bin_result], " Десятичный результат:", decimal_result)

    print("\nСложение чисел с плавающей точкой (для выхода введите 'e'):")
    while True:
        print("Ввод числа №1")
        input1 = input().strip()
        if input1.lower() == 'e':
            break
        try:
            num1 = float(input1.replace(',', '.'))
        except ValueError:
            print("Ошибка: введите число или 'e' для выхода.")
            continue

        print("Ввод числа №2")
        input2 = input().strip()
        if input2.lower() == 'e':
            break
        try:
            num2 = float(input2.replace(',', '.'))
        except ValueError:
            print("Ошибка: введите число или 'e' для выхода.")
            continue

        ieee1 = no.float_to_ieee754(num1)
        ieee2 = no.float_to_ieee754(num2)

        print(f"Число 1 в формате IEEE 754: [ {ieee1[0]} {ieee1[1:9]} {ieee1[9:]} ]")
        print(f"Число 2 в формате IEEE 754: [ {ieee2[0]} {ieee2[1:9]} {ieee2[9:]} ]")

        result_dec, result_bin = no.add_floating_point(num1, num2)
        print("Результат (десятичный):", result_dec)
        print(f"Результат (двоичный, IEEE 754): [ {result_bin[0]} {result_bin[1:9]} {result_bin[9:]} ]")


if __name__ == "__main__":
    main()