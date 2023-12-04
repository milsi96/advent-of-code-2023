import unittest
import logging
import sys

from day_2.main import Day2Solver

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


class TestDay2Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day2Solver().solve_first_problem('tests/resources/test_day_2_1.txt')
        self.assertEqual(result, 8)

    def test_can_solve_second_problem(self):
        result = Day2Solver().solve_second_problem('tests/resources/test_day_2_1.txt')
        self.assertEqual(result, 2286)
