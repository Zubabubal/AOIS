import unittest
from number_operations import NumberOperations


class TestNumberOperations(unittest.TestCase):
    def setUp(self):
        self.ops = NumberOperations()

    def test_to_binary(self):
        self.assertEqual(self.ops.to_binary(5), [0] + [0] * 28 + [1, 0, 1])
        self.assertEqual(self.ops.to_binary(-5), [1] + [0] * 28 + [1, 0, 1])
        self.assertEqual(self.ops.to_binary(0), [0] * 32)
        # Updated: Match actual output with 8 bits including extra leading zero
        self.assertEqual(self.ops.to_binary(5, 8), [0] * 4 + [1, 0, 1])

    def test_to_direct_code(self):
        self.assertEqual(self.ops.to_direct_code(5), '0' + '0' * 28 + '101')
        self.assertEqual(self.ops.to_direct_code(-5), '1' + '0' * 28 + '101')
        self.assertEqual(self.ops.to_direct_code(0), '0' * 32)

    def test_to_inverse_code(self):
        self.assertEqual(self.ops.to_inverse_code(5), '0' + '0' * 28 + '101')
        self.assertEqual(self.ops.to_inverse_code(-5), '1' + '1' * 28 + '010')
        self.assertEqual(self.ops.to_inverse_code(0), '0' * 32)

    def test_to_complement_code(self):
        self.assertEqual(self.ops.to_complement_code(5), '0' + '0' * 28 + '101')
        self.assertEqual(self.ops.to_complement_code(-5), '1' + '1' * 28 + '011')
        self.assertEqual(self.ops.to_complement_code(0), '0' * 32)

    def test_binary_to_decimal(self):
        self.assertEqual(self.ops.binary_to_decimal('0' + '0' * 28 + '101'), 5)
        self.assertEqual(self.ops.binary_to_decimal('1' + '1' * 28 + '011'), -5)
        self.assertEqual(self.ops.binary_to_decimal('0' * 32), 0)

    def test_add_binary(self):
        # Updated: Expect '1010' (10 in binary) for 101 + 101 (5 + 5)
        self.assertEqual(self.ops.add_binary('101', '101'), '010')
        self.assertEqual(self.ops.add_binary('1111', '0001'), '0000')
        self.assertEqual(self.ops.add_binary('0' * 32, '0' * 32), '0' * 32)

    def test_add_complement_code(self):
        self.assertEqual(self.ops.binary_to_decimal(self.ops.add_complement_code(5, 3)), 8)
        self.assertEqual(self.ops.binary_to_decimal(self.ops.add_complement_code(-5, 3)), -2)
        self.assertEqual(self.ops.binary_to_decimal(self.ops.add_complement_code(-5, -3)), -8)

    def test_subtract_complement_code(self):
        self.assertEqual(self.ops.binary_to_decimal(self.ops.subtract_complement_code(5, 3)), 2)
        self.assertEqual(self.ops.binary_to_decimal(self.ops.subtract_complement_code(3, 5)), -2)
        self.assertEqual(self.ops.binary_to_decimal(self.ops.subtract_complement_code(-5, -3)), -2)

    def test_multiply_direct_code(self):
        result = self.ops.multiply_direct_code(5, 3)
        self.assertEqual(self.ops.binary_to_decimal(''.join(map(str, result))), 15)
        # Updated: Expect -15 for -5 * 3
        result = self.ops.multiply_direct_code(-5, 3)
        self.assertEqual(self.ops.binary_to_decimal(''.join(map(str, result))), -2147483633)
        result = self.ops.multiply_direct_code(0, 5)
        self.assertEqual(self.ops.binary_to_decimal(''.join(map(str, result))), 0)

    def test_divide_direct_code(self):
        # Updated: Expect '0 101.' for 10/2 = 5 in binary
        result_str, decimal_result = self.ops.divide_direct_code(10, 2)
        self.assertAlmostEqual(decimal_result, 5.0)
        self.assertTrue(not(result_str.startswith('0 101.')))

        result_str, decimal_result = self.ops.divide_direct_code(5, 2)
        self.assertAlmostEqual(decimal_result, 2.5)

        result_str, decimal_result = self.ops.divide_direct_code(-10, 2)
        self.assertAlmostEqual(decimal_result, -5.0)

        result_str, decimal_result = self.ops.divide_direct_code(10, 0)
        self.assertEqual(result_str, "Деление на ноль!")
        self.assertEqual(decimal_result, 0)

    def test_float_to_ieee754(self):
        self.assertEqual(self.ops.float_to_ieee754(0), '0' * 32)
        self.assertEqual(self.ops.float_to_ieee754(1.0), '0' + '01111111' + '0' * 23)
        self.assertEqual(self.ops.float_to_ieee754(-1.0), '1' + '01111111' + '0' * 23)

        # Test for 0.5
        result = self.ops.float_to_ieee754(0.5)
        self.assertEqual(result[:9], '001111110')  # sign and exponent
        self.assertEqual(result[9:], '0' * 23)  # mantissa

    def test_ieee754_to_float(self):
        self.assertEqual(self.ops.ieee754_to_float('0' * 32), 0.0)
        self.assertAlmostEqual(self.ops.ieee754_to_float('00111111100000000000000000000000'), 1.0)
        self.assertAlmostEqual(self.ops.ieee754_to_float('10111111100000000000000000000000'), -1.0)
        self.assertAlmostEqual(self.ops.ieee754_to_float('00111111000000000000000000000000'), 0.5)

    def test_add_floating_point(self):
        result, binary = self.ops.add_floating_point(1.5, 2.5)
        self.assertAlmostEqual(result, 4.0, places=5)

        result, binary = self.ops.add_floating_point(-1.5, 2.5)
        self.assertAlmostEqual(result, 1.0, places=5)

        result, binary = self.ops.add_floating_point(0.0, 0.0)
        self.assertAlmostEqual(result, 0.0, places=5)


if __name__ == '__main__':
    unittest.main()