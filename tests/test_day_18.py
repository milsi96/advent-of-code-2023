import unittest

from day_18.main import Day18Solver, Direction


class TestDay18Solver(unittest.TestCase):
    def test_can_solve_first_problem(self):
        result = Day18Solver().solve_first_problem('tests/resources/test_day_18.txt')
        self.assertEqual(result, 62)

    def test_direction(self):
        move = Direction.move('L')
        self.assertEqual(move, (0, -1))

    def test_can_solve_second_problem(self):
        result = Day18Solver().solve_second_problem('tests/resources/test_day_18.txt')
        self.assertEqual(result, 952408144115)

    def test_convert_hex(self):
        result = int('70c710', 16)
        self.assertEqual(result, 7390992)
