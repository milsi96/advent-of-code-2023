import unittest

from custom_logger.custom_logger import CustomLogger
from day_9.main import Day9Solver

logger = CustomLogger(__name__).get_logger()


class TestDay8Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result1 = Day9Solver().solve_first_problem('tests/resources/test_day_9.txt')
        self.assertEqual(result1, 114)

    def test_can_solve_second_problem(self):
        result = Day9Solver().solve_second_problem('tests/resources/test_day_9.txt')
        self.assertEqual(result, 2)
