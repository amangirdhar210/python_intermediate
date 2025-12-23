import unittest
from main import divide, do_somthing
from unittest.mock import patch

class Test_Functions(unittest.TestCase):
    def test_divide(self):
        x=50
        y=5
        expected=10
        result=divide(x,y)
        self.assertEqual(result, expected)
        
    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(50,0)

    def test_decimal_places(self):
        x=50
        y=11
        expected=4.54
        result= divide(x,y)
        self.assertAlmostEqual(expected, result, delta=0.01)

    def test_do_something(self):
        num=50
        expected= 55.00
        with patch('main.function_to_mock') as mock_function:
            mock_function.return_value=1.1
            result= do_somthing(num)
            self.assertAlmostEqual(expected, result, delta=0.0001)

if __name__ == '__main__':
    unittest.main()