from typing import Tuple
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
        end_point = Point(len(lines) - 1, len(lines) - 1)
        costs, order = self.generate_heat_loss(city_map, Point(0, 0), end_point)

        path = self.reconstruct_path(order, start_point, end_point)
        logger.debug(" ".join(map(str, path)))

        logger.debug(f'Total cost is {costs[end_point]}')

        return costs[end_point]

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
        self,
        city_map: dict[Point, int],
        start: Point,
        end: Point,
    ) -> Tuple[dict[Point, int], dict[Point, Point]]:
        frontier: list[Point] = [start]
        cost_so_far: dict[Point, int] = {}
        cost_so_far[start] = 0
        came_from: dict[Point, Point] = {}

        while len(frontier) > 0:
            current_point: Point = frontier.pop(0)

            if current_point == end:
                break

            previous_points = self.reconstruct_path(came_from, start, current_point)

            for next_point in self.get_next_points(
                city_map, previous_points, current_point
            ):
                new_cost = cost_so_far[current_point] + city_map[next_point]
                if (
                    next_point not in cost_so_far.keys()
                    or new_cost < cost_so_far[next_point]
                ):
                    logger.debug(f'From {current_point} to {next_point} = {new_cost}')
                    cost_so_far[next_point] = new_cost
                    frontier.append(next_point)
                    came_from[next_point] = current_point

        return (cost_so_far, came_from)

    def reconstruct_path(
        self, came_from: dict[Point, Point], start: Point, end: Point
    ) -> list[Point]:
        current = end
        path: list[Point] = []
        if end not in came_from:
            return []

        while current != start:
            path.append(current)
            current = came_from[current]

        path.append(start)
        path.reverse()
        return path

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
