from laba import *
import unittest

class TestDigit(unittest.TestCase):
    def setUp(self):
        self.digit = Digit()

    def test_positive_bin(self):
        self.assertEqual(self.digit.positive_bin(10), '00000000000000000000000000001010')
        self.assertEqual(self.digit.positive_bin(0), '00000000000000000000000000000000')
        self.assertEqual(self.digit.positive_bin(255), '00000000000000000000000011111111')

    def test_negative_bin(self):
        self.assertEqual(self.digit.negative_bin(-10), '10000000000000000000000000001010')
        self.assertEqual(self.digit.negative_bin(-1), '10000000000000000000000000000001')

    def test_preadditional_summa(self):
        self.assertEqual(self.digit.preadditional_summa('0000000000000000000000000001010'), '0000000000000000000000000001011')
        self.assertEqual(self.digit.preadditional_summa('11111111111111111111111111110110'), '11111111111111111111111111110111')

    def test_binary_to_dec_num(self):
        self.assertEqual(self.digit.binary_to_dec_num('1010'), 10)
        self.assertEqual(self.digit.binary_to_dec_num('11111111'), 255)

    def test_convert_to_dec(self):
        self.assertEqual(self.digit.convert_to_dec('0000000000000000000000000001010'), 10)
        self.assertEqual(self.digit.convert_to_dec('11111111111111111111111111110110'), -10)

    def test_convert_to_binary_number(self):
        self.assertEqual(self.digit.convert_to_binary_number(10), '00000000000000000000000000001010')
        self.assertEqual(self.digit.convert_to_binary_number(-10), '10000000000000000000000000001010')

    def test_direct_code_to_int(self):
        self.assertEqual(self.digit.direct_code_to_int('0000000000000000000000000001010'), 10)
        self.assertEqual(self.digit.direct_code_to_int('11111111111111111111111111110110'), -2147483638)

    def test_float_to_binary_fraction(self):
        self.assertEqual(self.digit.float_to_binary_fraction(0.5), '1')
        self.assertEqual(self.digit.float_to_binary_fraction(0.25), '01')

    def test_convert_float_to_bin(self):
        self.assertEqual(self.digit.convert_float_to_bin(10.5), '01000001001010000000000000000000')
        self.assertEqual(self.digit.convert_float_to_bin(-10.5), '11000001001010000000000000000000')

    def test_convert_bin_to_float(self):
        self.assertAlmostEqual(self.digit.convert_bin_to_float('01000001001010000000000000000000'), 10.5)
        self.assertAlmostEqual(self.digit.convert_bin_to_float('11000001001010000000000000000000'), -10.5)

    def test_float_summa(self):
        self.assertAlmostEqual(self.digit.float_summa(10.5, 20.5), 31.0)
        self.assertAlmostEqual(self.digit.float_summa(-10.5, -20.5), -31.0)

    def test_display_ieee(self):
        # Этот метод просто печатает, поэтому мы просто вызываем его
        self.digit.display_ieee('01000001001010000000000000000000')

    def test_direct_summa(self):
        self.assertEqual(self.digit.direct_summa(10, 20), '00000000000000000000000000011110')
        self.assertEqual(self.digit.direct_summa(-10, -20), '00000000000000000000000000011110')
        self.assertEqual(self.digit.direct_summa(10, -20), '10000000000000000000000000011110')
        self.assertEqual(self.digit.direct_summa(-10, 20), '10000000000000000000000000011110')

    def test_convert_to_reverse_binary(self):
        self.assertEqual(self.digit.convert_to_reverse_binary(10), '00000000000000000000000000001010')
        self.assertEqual(self.digit.convert_to_reverse_binary(-10), '11111111111111111111111111110101')

    def test_convert_to_additional_binary(self):
        self.assertEqual(self.digit.convert_to_additional_binary(10), '00000000000000000000000000001010')
        self.assertEqual(self.digit.convert_to_additional_binary(-10), '11111111111111111111111111110110')

    def test_additional_summa(self):
        self.assertEqual(self.digit.additional_summa(10, 20), '00000000000000000000000000011110')
        self.assertEqual(self.digit.additional_summa(-10, -20), '11111111111111111111111111100010')
        self.assertEqual(self.digit.additional_summa(10, -20), '11111111111111111111111111110110')

    def test_additional_subtract(self):
        self.assertEqual(self.digit.additional_subtract(20, 10), '00000000000000000000000000001010')
        self.assertEqual(self.digit.additional_subtract(-20, -10), '11111111111111111111111111110110')
        self.assertEqual(self.digit.additional_subtract(10, 20), '11111111111111111111111111110110')

    def test_direct_code_multiplication(self):
        self.assertEqual(
            self.digit.direct_code_multiplication(10, 20),
            "Результат в прямом коде: [0000000000000000000000011001000]  Десятичный результат: 200"
        )
        self.assertEqual(
            self.digit.direct_code_multiplication(-10, 20),
            "Результат в прямом коде: [1000000000000000000000011001000]  Десятичный результат: -200"
        )

    def test_divide_bin(self):
        self.assertEqual(
            self.digit.divide_bin(20, 10),
            "Результат в прямом коде: [0 10.0]  Десятичный результат: 2"
        )
        self.assertEqual(
            self.digit.divide_bin(-20, 10),
            "Результат в прямом коде: [1 10.0]  Десятичный результат: -2"
        )

if __name__ == '__main__':
    unittest.main()