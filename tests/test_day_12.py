import unittest

from custom_logger.custom_logger import CustomLogger
from day_12.main import Arrangement, Condition, Day12Solver

logger = CustomLogger(__name__).get_logger()


class TestDay12Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result1 = Day12Solver().solve_first_problem('tests/resources/test_day_12.txt')
        self.assertEqual(result1, 21)

    @unittest.skip('tbd')
    def test_can_solve_second_problem(self):
        result1 = Day12Solver().solve_second_problem('tests/resources/test_day_12.txt')
        self.assertEqual(result1, 1030)

    def test_condition_are_initialized_correctly(self):
        condition1 = Condition.from_str('?')
        self.assertEqual(condition1, Condition.UNKNOWN)

        condition2 = Condition.from_str('.')
        self.assertEqual(condition2, Condition.OPERATIONAL)

        condition3 = Condition.from_str('#')
        self.assertEqual(condition3, Condition.DAMAGED)

    def test_indexes_are_correct(self):
        arrangement = Arrangement(['?', '?', '?', '.', '#', '#', '#'], [1, 1, 3])

        self.assertEqual(arrangement.damaged_springs_indexes, [4, 5, 6])
        self.assertEqual(arrangement.operational_springs_indexes, [3])
        self.assertEqual(arrangement.unknown_springs_indexes, [0, 1, 2])

    def test_get_next_arrangement(self):
        arrangement = Arrangement(
            [Condition.from_str(cond) for cond in '?#?#?#?#?#?#?#?'], [1, 1, 3]
        )

        arrangement.valid_arrangements
