import sys
from typing import Tuple
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver

logger = CustomLogger(__name__).get_logger()


class Day17Solver(Solver):
    lowest_heat_loss: int = sys.maxsize

    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        city_map: dict[Tuple[int, int], int] = {}
        cities: list[list[int]] = [
            [int(lines[row][column]) for column in range(len(lines[row]))]
            for row in range(len(lines))
        ]

        for row in range(len(cities)):
            for column in range(len(cities[row])):
                city_map[(row, column)] = cities[row][column]

        start_point = (0, 0)
        end_point = (len(lines) - 1, len(lines) - 1)
        came_from, cost_so_far = self.dijkstra_search(city_map, start_point, end_point)

        path = self.reconstruct_path(came_from, start_point, end_point)
        logger.debug(", ".join(map(str, path)))

        return self.get_heat_loss(city_map, path)

    def dijkstra_search(
        self,
        city_map: dict[Tuple[int, int], int],
        start: Tuple[int, int],
        end: Tuple[int, int],
    ) -> Tuple[dict[Tuple[int, int], Tuple[int, int]], dict[Tuple[int, int], int]]:
        frontier: list[Tuple[int, int]] = [start]
        came_from: dict[Tuple[int, int], Tuple[int, int]] = {}
        cost_so_far: dict[Tuple[int, int], int] = {}
        cost_so_far[start] = 0

        while len(frontier) > 0:
            current: Tuple[int, int] = frontier.pop(0)

            if current == end:
                break

            previous_points: list[Tuple[int, int]] = self.reconstruct_path(
                came_from, start, current
            )
            next_points = self.get_next_points(city_map, previous_points, current)
            for next in next_points:
                if not self.path_is_admissable(previous_points + [next]):
                    continue
                new_cost = cost_so_far[current] + city_map[next]
                if next not in cost_so_far.keys() or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    frontier.append(next)
                    came_from[next] = current

        return came_from, cost_so_far

    def reconstruct_path(
        self,
        came_from: dict[Tuple[int, int], Tuple[int, int]],
        start: Tuple[int, int],
        end: Tuple[int, int],
    ) -> list[Tuple[int, int]]:
        current = end
        path: list[Tuple[int, int]] = []
        if end not in came_from.keys():
            return []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def get_next_points(
        self,
        city_map: dict[Tuple[int, int], int],
        previous_points: list[Tuple[int, int]],
        point: Tuple[int, int],
    ) -> list[Tuple[int, int]]:
        ROW = 0
        COLUMN = 1
        next_points = [
            (point[ROW], point[COLUMN] + 1),
            (point[ROW], point[COLUMN] - 1),
            (point[ROW] - 1, point[COLUMN]),
            (point[ROW] + 1, point[COLUMN]),
        ]

        return list(
            filter(
                lambda p: p in city_map.keys() and p not in previous_points, next_points
            )
        )

    def path_is_admissable(self, points: list[Tuple[int, int]]) -> bool:
        ROW, COLUMN = 0, 1

        i = 0
        max_consequent_cubes = 5
        while i + max_consequent_cubes < len(points):
            if all(
                [p[ROW] == points[i][ROW] for p in points[i : i + max_consequent_cubes]]
            ):
                return False
            elif all(
                [
                    p[COLUMN] == points[i][COLUMN]
                    for p in points[i : i + max_consequent_cubes]
                ]
            ):
                return False

            i += 1

        return True

    def generate_heat_loss(
        self,
        city_map: dict[Tuple[int, int], int],
        previous_points: list[Tuple[int, int]],
        start: Tuple[int, int],
        end: Tuple[int, int],
    ) -> None:
        logger.debug(f'Trying all points from {start}')

        previous_points.append(start)
        next_points = self.get_next_points(city_map, previous_points, start)
        for point in next_points:
            if point == end:
                self.lowest_heat_loss = min(
                    self.get_heat_loss(city_map, previous_points) + city_map[end],
                    self.lowest_heat_loss,
                )
                logger.debug(f'Current lowest heat loss is {self.lowest_heat_loss}')
            else:
                if (
                    self.get_heat_loss(city_map, previous_points + [point])
                    > self.lowest_heat_loss
                ):
                    continue
                new_path = previous_points.copy()
                self.generate_heat_loss(city_map, new_path, point, end)

    def get_heat_loss(
        self, city_map: dict[Tuple[int, int], int], path: list[Tuple[int, int]]
    ) -> int:
        return sum([city_map[p] for p in path if p != (0, 0)])

    def solve_second_problem(self, file_name: str) -> int:
        return 0
