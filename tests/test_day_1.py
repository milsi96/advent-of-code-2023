import unittest
import logging
import sys

from day_1.main import Day1Solver

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


class TestDay1Solver(unittest.TestCase):

  def test_can_solve_first_problem(self):
    result = Day1Solver().solve_first_problem("tests/resources/test_day_1_1.txt")
    self.assertEqual(result, 142)

  def test_can_solve_second_problem(self):
    result = Day1Solver().solve_second_problem("tests/resources/test_day_1_2.txt")
    self.assertEqual(result, 281)

  def test_can_return_only_digits(self):
    line = 'pqr3stu8vwx'
    digits = Day1Solver()._get_all_digits(line)
    logger.debug(f'Digits found: {digits}')
    self.assertEqual(digits, [3, 8])

  def test_creates_correct_number(self):
    digits_list = [4, 2, 7]
    self.assertEqual(Day1Solver()._compose_number(digits_list), 47)

  def test_replaces_numbers_with_correct_digits(self):
    line = '4nineeightseven2'
    modified_line = Day1Solver()._replace_numbers(line)
    logger.debug(f'Line {line} became {modified_line}')
    self.assertEqual(modified_line, '49872')

    another_line = 'zoneight234'
    another_modified_line = Day1Solver()._replace_numbers(another_line)
    logger.debug(f'Line {another_line} became {another_modified_line}')
    self.assertEqual(another_modified_line, 'z1ight234')