import unittest

from day_6.main import Day6Solver


class TestDay6Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day6Solver().solve_first_problem('tests/resources/test_day_6.txt')
        self.assertEqual(result, 288)

    @unittest.skip
    def test_can_solve_second_problem(self):
        result = Day6Solver().solve_second_problem('tests/resources/test_day_6.txt')
        self.assertEqual(result, 71503)
