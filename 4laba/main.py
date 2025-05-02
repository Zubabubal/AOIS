from Builder import Builder
from Binary_helper import Binary_helper
from Minimizator import Minimizator
from constants import LITERALS, LEN_OF_TETRADA


def get_subtraction():
    values = [0] * 3  # A, B, C
    one = [0] * 2 + [1]
    literals = list(LITERALS[:3])  # A, B, C
    SDNF_D = []
    SDNF_P = []

    for i in range(2 ** 3):
        D = values[0] ^ values[1] ^ values[2]
        P = int((not values[0] and values[1]) or (not values[0] and values[2]) or (values[1] and values[2]))
        if D == 1:
            SDNF_D.append(Builder.build_SDNF(literals, values))
        if P == 1:
            SDNF_P.append(Builder.build_SDNF(literals, values))
        values = Binary_helper.sum_b(values, one)

    return "|".join(SDNF_D), "|".join(SDNF_P)


def get_D8421_2():
    values = [0] * LEN_OF_TETRADA
    one = [0] * (LEN_OF_TETRADA - 1) + [1]

    print('D8421\t\t\tD8421+2')
    for i in range(16):
        decimal = Binary_helper.calculate(values)
        if decimal > 13:
            y3, y2, y1, y0 = "X", "X", "X", "X"
        else:
            dec_plus2 = decimal + 2
            y3 = (dec_plus2 // 8) % 2
            y2 = (dec_plus2 // 4) % 2
            y1 = (dec_plus2 // 2) % 2
            y0 = dec_plus2 % 2
        print(f"{values[0]} {values[1]} {values[2]} {values[3]}\t\t\t{y3} {y2} {y1} {y0}")
        values = Binary_helper.sum_b(values, one)

    # Используем заданные минимизированные выражения
    min_Y = {
        "Y1": "(!C)",  # Y1 = !X1
        "Y2": "(!C&B)|(!B&C)",  # Y2 = (!X1&X2)|(!X2&X1)
        "Y3": "(!C&A)|(!B&A)|(!A&B&C)",  # Y3 = (!X1&X3)|(!X2&X3)|(!X3&X2&X1)
        "Y0": "(!C&D)|(!A&D)|(!B&D)"  # Y0 = (!X1&X0)|(!X3&X0)|(!X2&X0)
    }

    return min_Y


def replace(form):
    form = form.replace("A", "X3")
    form = form.replace("B", "X2")
    form = form.replace("C", "X1")
    form = form.replace("D", "X0")
    return form


def replace_back(form):
    form = form.replace("X3", "A")
    form = form.replace("X2", "B")
    form = form.replace("X1", "C")
    form = form.replace("X0", "D")
    return form


if __name__ == "__main__":
    SDNF_D, SDNF_P = get_subtraction()
    print("СДНФ для D: " + SDNF_D, "СДНФ для P: " + SDNF_P, sep='\n')
    print()

    min_Y = get_D8421_2()
    print(f"Y1 = {replace(min_Y['Y1'])}")
    print(f"Y2 = {replace(min_Y['Y2'])}")
    print(f"Y3 = {replace(min_Y['Y3'])}")
    print(f"Y0 = {replace(min_Y['Y0'])}")