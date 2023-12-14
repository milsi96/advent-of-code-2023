import unittest

from custom_logger.custom_logger import CustomLogger
from day_14.main import Day14Solver

logger = CustomLogger(__name__).get_logger()


class TestDay14Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day14Solver().solve_first_problem('tests/resources/test_day_14.txt')
        self.assertEqual(result, 136)

    @unittest.skip('tbd')
    def test_can_solve_second_problem(self):
        result = Day14Solver().solve_second_problem('tests/resources/test_day_14.txt')
        self.assertEqual(result, 400)

    def test_rock_is_moved_correctly(self):
        line1 = ['O', 'O', '.', '#', '.', 'O', '.', '.', '#', '#']
        new_index = Day14Solver().move_rock(line1, 5)
        self.assertEqual(new_index, 4)

        line2 = ['O', 'O', '.', '#', '.', 'O', '.', '.', '#', '#']
        new_index = Day14Solver().move_rock(line2, 1)
        self.assertEqual(new_index, 1)

        line3 = ['.', '.', '.', '.', 'O', '#', '.', 'O', '#', '.']
        new_index = Day14Solver().move_rock(line3, 4)
        self.assertEqual(new_index, 0)
