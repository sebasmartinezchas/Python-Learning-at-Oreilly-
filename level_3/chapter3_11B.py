import unittest
from chapter3_11 import Calculator

class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.calc=Calculator()

    def test_add_positive_number(self):
        result=self.calc.add(3,5)
        self.assertEqual(result,8)

    def test_multiply_zero(self):
        result=self.calc.multiply(5,0)
        self.assertEqual(result,0)
        self.assertEqual(len(self.calc.history),1)

    def test_multiple_operations(self):
        self.calc.add(2,3)
        self.calc.multiply(4,5)
        self.assertEqual(len(self.calc.history),2)
        self.assertIn("2 + 3 = 5",self.calc.history[0])
        self.assertIn("4 * 5 = 20",self.calc.history[1])




if __name__=='__main__':
    unittest.main()
