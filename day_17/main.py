from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver

logger = CustomLogger(__name__).get_logger()


class Point:
    row: int
    column: int

    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Point):
            return False
        return self.row == __value.row and self.column == __value.column

    def __hash__(self) -> int:
        return self.row + self.column * 3

    def __str__(self) -> str:
        return f'({self.row}, {self.column})'


class Day17Solver(Solver):
    heat_loss_store: dict[Point, int] = {}

    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        city_map: dict[Point, int] = {}
        cities: list[list[int]] = [
            [int(lines[row][column]) for column in range(len(lines[row]))]
            for row in range(len(lines))
        ]

        for row in range(len(cities)):
            for column in range(len(cities[row])):
                city_map[Point(row, column)] = cities[row][column]

        start_point = Point(0, 0)
        self.generate_heat_loss(city_map, [start_point], Point(0, 0))

        logger.debug(
            ', '.join(
                [
                    f'{str(point)}: {heat_loss}'
                    for point, heat_loss in self.heat_loss_store.items()
                ]
            )
        )

        return 0

    def get_next_points(
        self, city_map: dict[Point, int], previous_points: list[Point], point: Point
    ) -> list[Point]:
        next_points = [
            Point(point.row, point.column + 1),
            Point(point.row, point.column - 1),
            Point(point.row - 1, point.column),
            Point(point.row + 1, point.column),
        ]

        def point_is_admissable(point: Point) -> bool:
            if point not in city_map.keys() or point in previous_points:
                return False
            new_path = previous_points.copy()
            new_path.append(point)
            return self.path_is_admissable(new_path)

        return list(filter(point_is_admissable, next_points))

    def generate_heat_loss(
        self, city_map: dict[Point, int], previous_points: list[Point], point: Point
    ) -> int:
        if point in self.heat_loss_store:
            return self.heat_loss_store[point]

        next_points = self.get_next_points(city_map, previous_points, point)
        if len(next_points) == 0:
            self.heat_loss_store[point] = city_map[point]
            return city_map[point]

        logger.debug(f'Moves from {point} are {", ".join(map(str, next_points))}')

        for next_point in next_points:
            trial_path = previous_points.copy()
            trial_path.append(next_point)
            result = self.generate_heat_loss(city_map, trial_path, next_point)

            if point not in self.heat_loss_store.keys():
                self.heat_loss_store[point] = city_map[point] + result
            else:
                self.heat_loss_store[point] = min(self.heat_loss_store[point], result)

        return self.heat_loss_store[point]

    def path_is_admissable(self, path: list[Point]) -> bool:
        max_same_direction = 4
        last_point = path[-1]
        if len(path) < max_same_direction:
            return True

        same_direction_row = all(
            [p.row == last_point.row for p in path[-(max_same_direction + 1) : -1]]
        )
        same_direction_column = all(
            [
                p.column == last_point.column
                for p in path[-(max_same_direction + 1) : -1]
            ]
        )

        if same_direction_row or same_direction_column:
            return False
        return True

    def solve_second_problem(self, file_name: str) -> int:
        return 0
