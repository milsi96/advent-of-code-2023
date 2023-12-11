import unittest

from custom_logger.custom_logger import CustomLogger
from day_11.main import Day11Solver, Galaxy, Position

logger = CustomLogger(__name__).get_logger()


class TestDay11Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result1 = Day11Solver().solve_first_problem('tests/resources/test_day_11.txt')
        self.assertEqual(result1, 374)

    def test_can_solve_second_problem(self):
        result1 = Day11Solver().solve_second_problem(
            'tests/resources/test_day_11.txt', multiplier=10
        )
        self.assertEqual(result1, 1030)

        result1 = Day11Solver().solve_second_problem(
            'tests/resources/test_day_11.txt', multiplier=100
        )
        self.assertEqual(result1, 8410)

    def test_equality_between_galaxies(self):
        galaxy1 = Galaxy(1, Position(1, 4))
        galaxy2 = Galaxy(1, Position(1, 4))
        self.assertTrue(galaxy1 == galaxy2)

        galaxy3 = Galaxy(1, Position(1, 5))
        galaxy4 = Galaxy(1, Position(1, 4))
        self.assertFalse(galaxy3 == galaxy4)

    def test_distance_between_galaxies(self):
        galaxy1 = Galaxy(1, Position(0, 4))
        galaxy2 = Galaxy(1, Position(10, 9))
        self.assertEqual(galaxy1.distance(galaxy2), 15)
