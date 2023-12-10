import unittest

from custom_logger.custom_logger import CustomLogger
from day_10.main import Day10Solver, Position

logger = CustomLogger(__name__).get_logger()


class TestDay10Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result1 = Day10Solver().solve_first_problem('tests/resources/test_day_10_1.txt')
        self.assertEqual(result1, 4)

        result2 = Day10Solver().solve_first_problem('tests/resources/test_day_10_2.txt')
        self.assertEqual(result2, 8)

    def test_can_solve_second_problem(self):
        result1 = Day10Solver().solve_second_problem(
            'tests/resources/test_day_10_3.txt'
        )
        self.assertEqual(result1, 4)

        result2 = Day10Solver().solve_second_problem(
            'tests/resources/test_day_10_4.txt'
        )
        self.assertEqual(result2, 8)

        result3 = Day10Solver().solve_second_problem(
            'tests/resources/test_day_10_5.txt'
        )
        self.assertEqual(result3, 10)

    def test_correct_equality_for_points(self):
        point1 = Position(1, 2)
        point2 = Position(1, 2)
        self.assertTrue(point1 == point2)

        point3 = Position(2, 3)
        point4 = Position(3, 4)
        self.assertFalse(point3 == point4)
