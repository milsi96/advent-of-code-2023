import unittest

from custom_logger.custom_logger import CustomLogger
from day_14.main import Day14Solver

logger = CustomLogger(__name__).get_logger()


class TestDay14Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day14Solver().solve_first_problem('tests/resources/test_day_14.txt')
        self.assertEqual(result, 136)

    def test_can_solve_second_problem(self):
        result = Day14Solver().solve_second_problem('tests/resources/test_day_14.txt')
        self.assertEqual(result, 64)

    def test_rock_is_moved_correctly(self):
        line1 = ['O', 'O', '.', '#', '.', 'O', '.', '.', '#', '#']
        new_index = Day14Solver().move_rock_left(line1, 5)
        self.assertEqual(new_index, 4)

        line2 = ['O', 'O', '.', '#', '.', 'O', '.', '.', '#', '#']
        new_index = Day14Solver().move_rock_left(line2, 1)
        self.assertEqual(new_index, 1)

        line3 = ['.', '.', '.', '.', 'O', '#', '.', 'O', '#', '.']
        new_index = Day14Solver().move_rock_right(line3, 4)
        self.assertEqual(new_index, 4)

        line4 = ['.', '.', '.', '.', 'O', '#', '.', 'O', '#', 'O']
        new_index = Day14Solver().move_rock_right(line4, 9)
        self.assertEqual(new_index, 9)

        line5 = ['.', 'O', '.', '.', '.', '#', '.', 'O', '#', 'O']
        new_index = Day14Solver().move_rock_right(line5, 1)
        self.assertEqual(new_index, 4)
