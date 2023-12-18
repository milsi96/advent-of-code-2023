from enum import StrEnum
from typing import Tuple

from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver
import re
from shapely.geometry import Polygon


logger = CustomLogger(__name__).get_logger()


class Location:
    row: int
    column: int

    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def __hash__(self) -> int:
        return 2 * self.row + 5 * self.column

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Location):
            return False
        return self.row == __value.row and self.column == __value.column

    def __str__(self) -> str:
        return f'({self.row}, {self.column})'


class Direction(StrEnum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    @staticmethod
    def from_digit(digit: int) -> 'Direction':
        match digit:
            case 0:
                return Direction.RIGHT
            case 1:
                return Direction.DOWN
            case 2:
                return Direction.LEFT
            case 3:
                return Direction.UP

        raise ValueError(f'Value {digit} is not a valid direction')

    @staticmethod
    def move(direction: str, multiplier: int = 1) -> Tuple[int, int]:
        dir = Direction(direction)
        match dir:
            case Direction.UP:
                return (-1 * multiplier, 0)
            case Direction.DOWN:
                return (1 * multiplier, 0)
            case Direction.RIGHT:
                return (0, 1 * multiplier)
            case Direction.LEFT:
                return (0, -1 * multiplier)


class Day18Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        pattern = r'^(R|U|D|L)\s(\d+)\s\((#.{6})\)$'
        locations: list[Location] = []

        current_loc = Location(0, 0)
        locations.append(current_loc)
        for line in self.get_lines(file_name):
            dir, meters, _ = re.findall(pattern=pattern, string=line)[0]
            move = Direction.move(dir, multiplier=int(meters))
            logger.debug(f'Moving {dir} with {move}')

            new_row = current_loc.row + move[0]
            new_column = current_loc.column + move[1]

            current_loc = Location(new_row, new_column)
            locations.append(current_loc)
        locations.append(Location(0, 0))

        dig = Polygon([(loc.row, loc.column) for loc in locations])
        total_cubes = dig.area + (dig.length / 2) + 1

        logger.debug(f'Total cubes are {total_cubes}')

        return total_cubes

    def solve_second_problem(self, file_name: str) -> int:
        pattern = r'^.+\s\(#(.+)\)$'
        locations: list[Location] = []

        current_loc = Location(0, 0)
        locations.append(current_loc)
        for line in self.get_lines(file_name):
            color = re.findall(pattern=pattern, string=line)[0]
            meters = int(color[0:5], 16)
            dir = Direction.from_digit(int(color[-1]))
            move = Direction.move(dir, multiplier=int(meters))
            logger.debug(f'Moving {dir} with {move}')

            new_row = current_loc.row + move[0]
            new_column = current_loc.column + move[1]

            current_loc = Location(new_row, new_column)
            locations.append(current_loc)
        locations.append(Location(0, 0))

        dig = Polygon([(loc.row, loc.column) for loc in locations])
        total_cubes = dig.area + (dig.length / 2) + 1

        logger.debug(f'Total cubes are {total_cubes}')

        return int(total_cubes)


if __name__ == '__main__':
    Day18Solver().solve_first_problem("day_18/input.txt")
    Day18Solver().solve_second_problem("day_18/input.txt")
