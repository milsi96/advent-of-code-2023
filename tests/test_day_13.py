import unittest

from custom_logger.custom_logger import CustomLogger
from day_13.main import Day13Solver, Pattern, Point, Note

logger = CustomLogger(__name__).get_logger()


class TestDay13Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day13Solver().solve_first_problem('tests/resources/test_day_13.txt')
        self.assertEqual(result, 405)

    def test_can_solve_second_problem(self):
        result = Day13Solver().solve_second_problem('tests/resources/test_day_13.txt')
        self.assertEqual(result, 400)

    def test_differences_are_found_correctly(self) -> None:
        line1 = [Point(0, 0, Pattern(ch)) for ch in '#...##..#']
        line2 = [Point(0, 0, Pattern(ch)) for ch in '#....#..#']
        diff = Note.difference(line1, line2)

        self.assertEqual(diff, 1)

    def test_points_are_equal(self) -> None:
        point1 = Point(1, 2, Pattern.ROCK)
        point2 = Point(1, 2, Pattern.ASH)
        self.assertFalse(point1 == point2)

        point3 = Point(1, 2, Pattern.ASH)
        point4 = Point(1, 2, Pattern.ASH)
        self.assertTrue(point3 == point4)
