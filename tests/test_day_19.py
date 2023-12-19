import unittest

from day_19.main import Day19Solver


class TestDay19Solver(unittest.TestCase):
    def setUp(self) -> None:
        self.test_input_file = 'tests/resources/test_day_19.txt'

    def test_can_solve_first_problem(self) -> None:
        Day19Solver().solve_first_problem(self.test_input_file)
