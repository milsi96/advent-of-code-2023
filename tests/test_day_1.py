import unittest
import logging
import sys

from day_1.main import Day1Solver

logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


class TestDay1Solver(unittest.TestCase):

  def test_can_find_digits(self):
    result = Day1Solver().solve_first_problem("tests/resources/test_day_1.txt")
    self.assertEqual(result, 142)
