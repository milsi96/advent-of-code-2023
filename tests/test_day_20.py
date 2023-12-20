import unittest

from day_20.main import Day20Solver


class TestDay20Solver(unittest.TestCase):
    def setUp(self) -> None:
        self.first_input = 'tests/resources/test_day_20_1.txt'
        self.second_input = 'tests/resources/test_day_20_2.txt'

    def test_can_solve_first_problem(self) -> None:
        result1 = Day20Solver().solve_first_problem(self.first_input)
        self.assertEqual(result1, 32000000)

        result2 = Day20Solver().solve_first_problem(self.second_input)
        self.assertEqual(result2, 11687500)
