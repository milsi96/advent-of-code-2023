import unittest

from custom_logger.custom_logger import CustomLogger
from day_17.main import Day17Solver

logger = CustomLogger(__name__).get_logger()


class TestDay17Solver(unittest.TestCase):
    def setUp(self) -> None:
        self.city_map = Day17Solver().generate_map(
            Day17Solver().get_lines('tests/resources/test_day_17.txt')
        )

    def test_can_solve_first_problem(self) -> None:
        result = Day17Solver().solve_first_problem('tests/resources/test_day_17.txt')
        self.assertEqual(result, 102)
