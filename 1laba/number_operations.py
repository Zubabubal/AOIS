class NumberOperations:
    def __init__(self):
        self.TOTAL_BITS = 32
        self.MAX_BITS = 31
        self.EXPONENT_BITS = 127
        self.MANTISSA_BITS = 23

    def to_binary(self, n, bits=32):
        if n == 0:
            return [0] * bits
        sign = 0 if n >= 0 else 1
        abs_n = abs(n)
        binary = []
        while abs_n > 0:
            binary.append(abs_n % 2)
            abs_n = abs_n // 2
        binary = binary[::-1]
        while len(binary) < bits - 1:
            binary.insert(0, 0)
        return [sign] + binary if bits == 32 else binary

    def to_direct_code(self, n):
        binary = self.to_binary(n)
        return ''.join(map(str, binary))

    def to_inverse_code(self, n):
        if n >= 0:
            return self.to_direct_code(n)
        abs_n = abs(n)
        binary = self.to_binary(abs_n)
        inverted = [1 - bit for bit in binary[1:]]
        return '1' + ''.join(map(str, inverted))

    def to_complement_code(self, n):
        if n >= 0:
            return self.to_direct_code(n)
        inverse = self.to_inverse_code(n)
        # Добавляем 1 к обратному коду
        carry = 1
        complement = list(inverse)
        for i in range(len(complement) - 1, 0, -1):
            if complement[i] == '0' and carry == 1:
                complement[i] = '1'
                carry = 0
                break
            elif complement[i] == '1' and carry == 1:
                complement[i] = '0'
        return ''.join(complement)

    def binary_to_decimal(self, binary_str):
        if binary_str[0] == '0':
            return int(binary_str, 2)
        else:
            # Для дополнительного кода
            inverted = ''.join('1' if b == '0' else '0' for b in binary_str[1:])
            return -(int(inverted, 2) + 1)

    def add_binary(self, a, b):
        max_len = max(len(a), len(b))
        a = a.zfill(max_len)
        b = b.zfill(max_len)
        carry = 0
        result = []
        for i in range(max_len - 1, -1, -1):
            sum_bits = int(a[i]) + int(b[i]) + carry
            result.append(str(sum_bits % 2))
            carry = sum_bits // 2
        if carry:
            result.append('1')
        return ''.join(reversed(result))[-max_len:]

    def add_complement_code(self, a, b):
        a_bin = self.to_complement_code(a)
        b_bin = self.to_complement_code(b)
        result = self.add_binary(a_bin, b_bin)
        return result

    def subtract_complement_code(self, a, b):
        return self.add_complement_code(a, -b)

    def multiply_direct_code(self, a, b):
        sign = 0 if (a >= 0) == (b >= 0) else 1
        abs_a = abs(a)
        abs_b = abs(b)
        product = abs_a * abs_b
        binary = self.to_binary(product if sign == 0 else -product)
        return binary

    def divide_direct_code(self, a, b, precision=13):
        if b == 0:
            return "Деление на ноль!", 0
        sign = 0 if (a >= 0) == (b >= 0) else 1
        abs_a = abs(a)
        abs_b = abs(b)

        # Более точное вычисление
        decimal_result = round(a / b, 6)  # 6 знаков после запятой

        # Для бинарного представления
        quotient = abs_a // abs_b
        remainder = abs_a % abs_b
        fractional = []
        for _ in range(precision):
            remainder *= 2
            bit = 1 if remainder >= abs_b else 0
            fractional.append(bit)
            if bit == 1:
                remainder -= abs_b

        integer_part = self.to_binary(quotient, 32)[1:]
        result_str = f"{sign} {''.join(map(str, integer_part))}.{''.join(map(str, fractional))}"
        return result_str, decimal_result

    def float_to_ieee754(self, num):
        if num == 0:
            return '0' * 32

        sign = '0' if num >= 0 else '1'
        abs_num = abs(num)

        # Особый случай для целых чисел
        if abs_num.is_integer():
            integer = int(abs_num)
            if integer == 0:
                return '0' * 32
            exponent = 0
            while integer >= 2:
                integer >>= 1
                exponent += 1
            mantissa = integer - 1
            biased_exp = exponent + self.EXPONENT_BITS
            return sign + bin(biased_exp)[2:].zfill(8) + '0' * 23

        # Обычный случай для дробных чисел
        exponent = 0
        if abs_num >= 2:
            while abs_num >= 2:
                abs_num /= 2
                exponent += 1
        else:
            while abs_num < 1:
                abs_num *= 2
                exponent -= 1

        mantissa = abs_num - 1
        mant_bin = ''
        for _ in range(self.MANTISSA_BITS):
            mantissa *= 2
            mant_bin += '1' if mantissa >= 1 else '0'
            if mantissa >= 1:
                mantissa -= 1

        biased_exp = exponent + self.EXPONENT_BITS
        exp_bin = bin(biased_exp)[2:].zfill(8)
        return sign + exp_bin + mant_bin

    def ieee754_to_float(self, binary):
        if binary == '0' * 32:
            return 0.0
        sign = -1 if binary[0] == '1' else 1
        exponent = int(binary[1:9], 2) - self.EXPONENT_BITS
        mantissa = 1.0
        for i, bit in enumerate(binary[9:32]):
            mantissa += int(bit) * (2 ** -(i + 1))
        return sign * mantissa * (2 ** exponent)

    def add_floating_point(self, a, b):
        a_dec = self.ieee754_to_float(self.float_to_ieee754(a))
        b_dec = self.ieee754_to_float(self.float_to_ieee754(b))
        result = a_dec + b_dec
        return round(result, 5), self.float_to_ieee754(result)