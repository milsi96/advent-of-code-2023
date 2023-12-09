import unittest
from day_2.main import Day2Solver
from custom_logger.custom_logger import CustomLogger

logger = CustomLogger(__name__).get_logger()


class TestDay2Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day2Solver().solve_first_problem('tests/resources/test_day_2_1.txt')
        self.assertEqual(result, 8)

    def test_can_solve_second_problem(self):
        result = Day2Solver().solve_second_problem('tests/resources/test_day_2_1.txt')
        self.assertEqual(result, 2286)
