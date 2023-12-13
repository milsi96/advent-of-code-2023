import unittest

from custom_logger.custom_logger import CustomLogger
from day_13.main import Day13Solver

logger = CustomLogger(__name__).get_logger()


class TestDay13Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        Day13Solver().solve_first_problem('tests/resources/test_day_13.txt')

    def test_can_solve_second_problem(self):
        Day13Solver().solve_second_problem('tests/resources/test_day_13.txt')
