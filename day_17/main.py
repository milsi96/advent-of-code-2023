from typing import Tuple
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver

logger = CustomLogger(__name__).get_logger()

Point = Tuple[int, int]


class Day17Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        city_map: dict[Point, int] = self.generate_map(self.get_lines(file_name))

        logger.debug(city_map)

        came_from, cost_so_far = self.dijkstra_search(city_map, (0, 0), (12, 12))

        path = self.reconstruct_path(came_from, (0, 0), (12, 12))

        logger.debug(" ".join(map(str, path)))

        logger.debug(cost_so_far[(1, 5)])
        logger.debug(cost_so_far[(2, 4)])

        return cost_so_far[(12, 12)]

    def generate_map(self, lines: list[str]) -> dict[Point, int]:
        city_map: dict[Point, int] = {}
        for row in range(len(lines)):
            for column in range(len(lines[row])):
                city_map[(row, column)] = int(lines[row][column])
        return city_map

    def dijkstra_search(
        self, city_map: dict[Point, int], start: Point, end: Point
    ) -> Tuple[dict[Point, Point], dict[Point, int]]:
        frontier: list[Point] = [start]
        came_from: dict[Point, Point] = {}
        cost_so_far: dict[Point, int] = {}
        cost_so_far[start] = 0

        ROW = 0
        COLUMN = 1

        while len(frontier):
            current: Point = frontier.pop(0)

            last_five_points = self.reconstruct_path(came_from, start, current)[-5:]
            if len(last_five_points) == 5:
                if all([last_five_points[-1][ROW] == p[ROW] for p in last_five_points]):
                    continue
                if all(
                    [
                        last_five_points[-1][COLUMN] == p[COLUMN]
                        for p in last_five_points
                    ]
                ):
                    continue

            if current == end:
                break

            next_points = [
                (current[ROW], current[COLUMN] + 1),
                (current[ROW], current[COLUMN] - 1),
                (current[ROW] + 1, current[COLUMN]),
                (current[ROW] - 1, current[COLUMN]),
            ]

            for next in next_points:
                if next not in city_map:
                    continue
                new_cost = cost_so_far[current] + city_map[next]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    frontier.append(next)
                    came_from[next] = current

        return came_from, cost_so_far

    def reconstruct_path(
        self, came_from: dict[Point, Point], start: Point, goal: Point
    ) -> list[Point]:
        current: Point = goal
        path: list[Point] = []
        if goal not in came_from:
            return []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def solve_second_problem(self, file_name: str) -> int:
        return 0
