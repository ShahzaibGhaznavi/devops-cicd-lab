```python
import unittest

from app import calculate_total, main


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

    def test_decimal_price(self):
        self.assertEqual(calculate_total(10.5, 2), 21.0)

    def test_main_prints_total(self):
        from io import StringIO
        from contextlib import redirect_stdout

        output = StringIO()

        with redirect_stdout(output):
            main()

        self.assertEqual(output.getvalue(), "Total price: 300\n")


if __name__ == "__main__":
    unittest.main()
```
