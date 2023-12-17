import unittest

from custom_logger.custom_logger import CustomLogger
from day_17.main import Day17Solver, Point
from file_reader.file_reader import FileReader

logger = CustomLogger(__name__).get_logger()


class TestDay17Solver(unittest.TestCase):
    def test_can_solve_first_problem(self) -> None:
        result = Day17Solver().solve_first_problem('tests/resources/test_day_17.txt')
        self.assertEqual(result, 102)

    def test_path_is_correct(self) -> None:
        lines = FileReader().get_lines('tests/resources/test_day_17.txt')
        city_map: dict[Point, int] = {}
        cities: list[list[int]] = [
            [int(lines[row][column]) for column in range(len(lines[row]))]
            for row in range(len(lines))
        ]

        for row in range(len(cities)):
            for column in range(len(cities[row])):
                city_map[Point(row, column)] = cities[row][column]

        start_point = Point(0, 0)
        end_point = Point(len(lines) - 1, len(lines) - 1)
        solver = Day17Solver()
        solver.generate_heat_loss(city_map, [start_point], start_point, end_point)
        for point, min_heat_loss in solver.heat_loss_store.items():
            logger.debug(f'{point} -> {min_heat_loss}')
