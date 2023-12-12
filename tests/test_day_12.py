import unittest

from custom_logger.custom_logger import CustomLogger
from day_12.main import Arrangement, Condition, Day12Solver
from file_reader.file_reader import FileReader

logger = CustomLogger(__name__).get_logger()


class TestDay12Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result1 = Day12Solver().solve_first_problem('tests/resources/test_day_12.txt')
        self.assertEqual(result1, 21)

    def test_can_solve_second_problem(self):
        result1 = Day12Solver().solve_second_problem('tests/resources/test_day_12.txt')
        self.assertEqual(result1, 525152)

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

    def test_correct_arrangements_number(self) -> None:
        lines = FileReader().get_lines('tests/resources/test_day_12.txt')
        arrangements: list[Arrangement] = []

        for line in lines:
            conditions = [cond for cond in line.split(' ')[0]]
            arrangements.append(
                Arrangement(
                    [Condition.from_str(cond) for cond in conditions],
                    [int(num) for num in line.split(' ')[1].split(',')],
                )
            )

        self.assertEqual(arrangements[0].valid_arrangements, 1)
        self.assertEqual(arrangements[1].valid_arrangements, 4)
        self.assertEqual(arrangements[2].valid_arrangements, 1)
        self.assertEqual(arrangements[3].valid_arrangements, 1)
        self.assertEqual(arrangements[4].valid_arrangements, 4)
        self.assertEqual(arrangements[5].valid_arrangements, 10)

        arr1 = Arrangement(
            [Condition.from_str(cond) for cond in '?#?#?#?#?#?#?#?'],
            [1, 3, 1, 6],
        )
        logger.debug(arr1.valid_arrangements_unfolded)

    def test_correct_arrangements_when_unfolded(self) -> None:
        lines = FileReader().get_lines('tests/resources/test_day_12.txt')
        arrangements: list[Arrangement] = []

        for line in lines:
            conditions = [cond for cond in line.split(' ')[0]]
            arrangements.append(
                Arrangement(
                    [Condition.from_str(cond) for cond in conditions],
                    [int(num) for num in line.split(' ')[1].split(',')],
                )
            )

        self.assertEqual(arrangements[0].valid_arrangements_unfolded, 1)
        self.assertEqual(arrangements[1].valid_arrangements_unfolded, 16384)
        self.assertEqual(arrangements[2].valid_arrangements_unfolded, 1)
        self.assertEqual(arrangements[3].valid_arrangements_unfolded, 16)
        self.assertEqual(arrangements[4].valid_arrangements_unfolded, 2500)
        self.assertEqual(arrangements[5].valid_arrangements_unfolded, 506250)

    def test_arrangement_is_valid(self):
        valid1 = Arrangement.is_valid(
            [Condition.from_str(cond) for cond in '.#.#.#######.##'], [1, 3, 1, 6]
        )
        self.assertEqual(valid1, False)

        valid2 = Arrangement.is_valid(
            [Condition.from_str(cond) for cond in '.#.#.#########.'], [1, 3, 1, 6]
        )
        self.assertEqual(valid2, False)

        valid3 = Arrangement.is_valid(
            [Condition.from_str(cond) for cond in '.###.....###'], [3, 2, 1]
        )
        self.assertEqual(valid3, False)
