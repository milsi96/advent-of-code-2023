import unittest
import logging
import sys

from day_5.main import Day5Solver
from file_reader.file_reader import FileReader

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class TestDay5Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day5Solver().solve_first_problem('tests/resources/test_day_5_1.txt')
        logger.debug(f'Result {result}')
        self.assertEqual(result, 35)

    def test_returns_correct_destination(self):
        lines = FileReader().get_lines('tests/resources/test_day_5_1.txt')
        _, maps = Day5Solver()._parse_lines(lines)

        self.assertEqual(maps['seed'].get_destination(79), 81)
        self.assertEqual(maps['seed'].get_destination(13), 13)

    def test_can_solve_second_problem(self):
        result = Day5Solver().solve_second_problem('tests/resources/test_day_5_1.txt')
        logger.debug(f'Result {result}')
        self.assertEqual(result, 46)
