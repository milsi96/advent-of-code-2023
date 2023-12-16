import unittest
from custom_logger.custom_logger import CustomLogger

from day_16.main import Day16Solver, Direction
from file_reader.file_reader import FileReader

logger = CustomLogger(__name__).get_logger()


class TestDay16Solver(unittest.TestCase):
    def test_can_solve_first_problem(self) -> None:
        result = Day16Solver().solve_first_problem('tests/resources/test_day_16.txt')
        self.assertEqual(result, 46)

    def test_tiles_are_moved_correctly(self) -> None:
        contraption = Day16Solver().parse_contraption(
            FileReader().get_lines('tests/resources/test_day_16.txt')
        )

        # test empty space
        move1 = Day16Solver().next_tiles(contraption, Direction.DOWN, contraption[0][0])
        if move1 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(move1[0].next_tile, contraption[1][0])

        # test mirror 45
        move2 = Day16Solver().next_tiles(contraption, Direction.DOWN, contraption[1][4])
        if move2 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(move2[0].next_tile, contraption[1][5])

        # test mirror 135
        move3 = Day16Solver().next_tiles(contraption, Direction.DOWN, contraption[6][4])
        if move3 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(move3[0].next_tile, contraption[6][3])

        # test vertical splitter
        move4 = Day16Solver().next_tiles(
            contraption, Direction.RIGHT, contraption[2][5]
        )
        if move4 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertIn(contraption[1][5], [move.next_tile for move in move4])
        self.assertIn(contraption[3][5], [move.next_tile for move in move4])

        # test horizontal splitter
        move5 = Day16Solver().next_tiles(
            contraption, Direction.RIGHT, contraption[7][3]
        )
        if move5 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(len(move5), 1)
        self.assertIn(contraption[7][4], [move.next_tile for move in move5])

        # test horizontal splitter
        move6 = Day16Solver().next_tiles(contraption, Direction.UP, contraption[7][3])
        if move6 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(len(move6), 2)
        self.assertIn(contraption[7][2], [move.next_tile for move in move6])

        # test horizontal splitter
        move6 = Day16Solver().next_tiles(contraption, Direction.DOWN, contraption[7][1])
        if move6 is None:
            error = 'Move should be not None'
            logger.error(error)
            raise AssertionError(error)
        self.assertEqual(len(move6), 2)
        self.assertIn(contraption[7][2], [move.next_tile for move in move6])
