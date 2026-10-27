
import unittest

from app import calculate_total


class TestCalculateTotal(unittest.TestCase):

    def test_calculate_total(self):
        self.assertEqual(calculate_total(100, 3), 300)

    def test_zero_quantity(self):
        self.assertEqual(calculate_total(100, 0), 0)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            calculate_total(-100, 2)

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            calculate_total(100, -2)


if __name__ == "__main__":
    unittest.main()
