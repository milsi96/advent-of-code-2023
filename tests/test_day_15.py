import unittest
from custom_logger.custom_logger import CustomLogger

from day_15.main import Day15Solver

logger = CustomLogger(__name__).get_logger()


class TestDay15Solver(unittest.TestCase):
    def test_can_solve_first_problem(self) -> None:
        result = Day15Solver().solve_first_problem('tests/resources/test_day_15.txt')
        self.assertEqual(result, 1320)

    def test_hash_is_correct(self) -> None:
        token = 'HASH'
        result = Day15Solver().calculate_hash(token)
        self.assertEqual(result, 52)

    def test_can_solve_second_problem(self) -> None:
        Day15Solver().solve_second_problem('tests/resources/test_day_15.txt')
