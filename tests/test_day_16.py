import unittest
from custom_logger.custom_logger import CustomLogger

from day_16.main import Day16Solver, Direction, Move
from file_reader.file_reader import FileReader

logger = CustomLogger(__name__).get_logger()


class TestDay16Solver(unittest.TestCase):
    def setUp(self) -> None:
        self.contraption = Day16Solver().parse_contraption(
            FileReader().get_lines('tests/resources/test_day_16.txt')
        )
        return super().setUp()

    def test_can_solve_first_problem(self) -> None:
        result = Day16Solver().solve_first_problem('tests/resources/test_day_16.txt')
        self.assertEqual(result, 46)

    def test_can_solve_second_problem(self) -> None:
        pass

    def test_energized_beam_are_correct(self):
        first_move = Move(Direction.DOWN, self.contraption[0][3])
        result = Day16Solver().energized_beams(self.contraption, first_move)
        self.assertEqual(result, 51)

    def test_move_from_empty_space(self):
        move1 = Day16Solver().next_tiles(
            self.contraption, Direction.DOWN, self.contraption[0][0]
        )
        if move1 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(move1[0].next_tile, self.contraption[1][0])

    def test_move_from_mirror_45(self):
        move2 = Day16Solver().next_tiles(
            self.contraption, Direction.DOWN, self.contraption[1][4]
        )
        if move2 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(move2[0].next_tile, self.contraption[1][5])

    def test_move_from_mirror_135(self):
        move3 = Day16Solver().next_tiles(
            self.contraption, Direction.DOWN, self.contraption[6][4]
        )
        if move3 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(move3[0].next_tile, self.contraption[6][3])

    def test_move_from_vertical_splitter(self):
        move4 = Day16Solver().next_tiles(
            self.contraption, Direction.RIGHT, self.contraption[2][5]
        )
        if move4 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertIn(self.contraption[1][5], [move.next_tile for move in move4])
        self.assertIn(self.contraption[3][5], [move.next_tile for move in move4])

    def test_move_from_horizontal_splitter(self):
        move5 = Day16Solver().next_tiles(
            self.contraption, Direction.RIGHT, self.contraption[7][3]
        )
        if move5 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(len(move5), 1)
        self.assertIn(self.contraption[7][4], [move.next_tile for move in move5])

        move6 = Day16Solver().next_tiles(
            self.contraption, Direction.UP, self.contraption[7][3]
        )
        if move6 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(len(move6), 2)
        self.assertIn(self.contraption[7][2], [move.next_tile for move in move6])

        move6 = Day16Solver().next_tiles(
            self.contraption, Direction.DOWN, self.contraption[7][1]
        )
        if move6 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(len(move6), 2)
        self.assertIn(self.contraption[7][2], [move.next_tile for move in move6])
