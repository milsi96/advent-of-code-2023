import unittest

from custom_logger.custom_logger import CustomLogger
from day_8.main import Day8Solver

logger = CustomLogger(__name__).get_logger()


class TestDay8Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result1 = Day8Solver().solve_first_problem('tests/resources/test_day_8_1.txt')
        self.assertEqual(result1, 2)

        result2 = Day8Solver().solve_first_problem('tests/resources/test_day_8_2.txt')
        self.assertEqual(result2, 6)

    def test_can_solve_second_problem(self):
        result = Day8Solver().solve_second_problem('tests/resources/test_day_8_3.txt')
        self.assertEqual(result, 6)
