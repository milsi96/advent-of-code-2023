from typing import Tuple
import unittest

from custom_logger.custom_logger import CustomLogger
from day_17.main import Day17Solver

logger = CustomLogger(__name__).get_logger()


class TestDay17Solver(unittest.TestCase):
    def setUp(self) -> None:
        lines = Day17Solver().get_lines('tests/resources/test_day_17.txt')
        city_map: dict[Tuple[int, int], int] = {}
        cities: list[list[int]] = [
            [int(lines[row][column]) for column in range(len(lines[row]))]
            for row in range(len(lines))
        ]

        for row in range(len(cities)):
            for column in range(len(cities[row])):
                city_map[(row, column)] = cities[row][column]

        self.city_map = city_map

    def test_can_solve_first_problem(self) -> None:
        result = Day17Solver().solve_first_problem('tests/resources/test_day_17.txt')
        self.assertEqual(result, 102)

    def test_fewest_heat_loss(self) -> None:
        path = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (0, 5),
            (0, 6),
            (0, 7),
            (0, 8),
            (1, 8),
            (2, 8),
            (2, 9),
            (2, 10),
            (3, 10),
            (4, 10),
            (4, 11),
            (5, 11),
            (6, 11),
            (7, 11),
            (7, 12),
            (8, 12),
            (9, 12),
            (10, 12),
            (10, 11),
            (11, 11),
            (12, 11),
            (12, 12),
        ]
        heat_loss = Day17Solver().get_heat_loss(self.city_map, path)
        self.assertEqual(heat_loss, 102)

    def test_path_is_admissable(self) -> None:
        path1 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)]
        admissable = Day17Solver().path_is_admissable(path1)
        self.assertEqual(admissable, True)

        path2 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
        admissable = Day17Solver().path_is_admissable(path2)
        self.assertEqual(admissable, False)
