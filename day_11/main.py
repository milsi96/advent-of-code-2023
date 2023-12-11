from typing import Any
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver


logger = CustomLogger(__name__).get_logger()


class Position:
    row: int
    column: int

    def __init__(self, row: int, column: int):
        if row < 0 or column < 0:
            error = 'Row and column must be greater or equal than 0,'
            error = error + f' got row {row} and column {column}'
            logger.error(error)
            raise ValueError(error)

        self.row = row
        self.column = column

    def __eq__(self, other: Any):
        if isinstance(other, Position):
            return self.row == other.row and self.column == other.column
        return False

    def __str__(self) -> str:
        return f'({self.row}, {self.column})'


class Galaxy:
    id: int
    position: Position

    def __init__(self, id: int, position: Position):
        self.id = id
        self.position = position

    def __str__(self) -> str:
        return f'Galaxy {self.id}: position {self.position}'

    def __eq__(self, __value: Any) -> bool:
        if isinstance(__value, Galaxy):
            return self.id == __value.id and self.position == __value.position
        else:
            return False

    def distance(self, other: 'Galaxy') -> int:
        return (
            max(self.position.row, other.position.row)
            - min(self.position.row, other.position.row)
        ) + (
            max(self.position.column, other.position.column)
            - min(self.position.column, other.position.column)
        )


class Day11Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        galaxies = self.parse_lines(lines)

        ground_rows = self.get_all_ground_rows(lines)
        ground_columns = self.get_all_ground_columns(lines)

        logger.debug(f'Ground rows: {ground_rows}')
        logger.debug(f'Ground columns: {ground_columns}')

        for galaxy in galaxies.values():
            rows_to_increment = sum(
                [galaxy.position.row >= ground_row for ground_row in ground_rows]
            )
            columns_to_increment = sum(
                [
                    galaxy.position.column >= ground_column
                    for ground_column in ground_columns
                ]
            )
            galaxy.position.row += rows_to_increment
            galaxy.position.column += columns_to_increment

        logger.debug(', '.join([str(galaxy) for galaxy in galaxies.values()]))

        distance = 0
        for i in sorted(galaxies.keys()):
            for j in sorted(galaxies.keys()):
                if j <= i:
                    continue
                distance += galaxies[i].distance(galaxies[j])

        logger.debug(f'Distance: {distance}')

        return distance

    def get_all_ground_rows(self, lines: list[str]) -> list[int]:
        ground_rows: list[int] = []
        for i in range(len(lines)):
            if all([ch == '.' for ch in lines[i]]):
                ground_rows.append(i)
        return ground_rows

    def get_all_ground_columns(self, lines: list[str]) -> list[int]:
        ground_columns: list[int] = []
        transposed_lines = [
            [lines[j][i] for j in range(len(lines))] for i in range(len(lines[0]))
        ]
        for i in range(len(transposed_lines)):
            if all([ch == '.' for ch in transposed_lines[i]]):
                ground_columns.append(i)
        return ground_columns

    def parse_lines(self, lines: list[str]) -> dict[int, Galaxy]:
        result: dict[int, Galaxy] = {}
        ids = 1
        for row in range(len(lines)):
            for column in range(len(lines[row])):
                if lines[row][column] != '#':
                    continue
                result[ids] = Galaxy(ids, Position(row, column))
                ids += 1

        return result

    def solve_second_problem(self, file_name: str, multiplier: int = 1) -> int:
        lines = self.get_lines(file_name)
        galaxies = self.parse_lines(lines)

        ground_rows = self.get_all_ground_rows(lines)
        ground_columns = self.get_all_ground_columns(lines)

        logger.debug(f'Ground rows: {ground_rows}')
        logger.debug(f'Ground columns: {ground_columns}')

        for galaxy in galaxies.values():
            rows_to_increment = sum(
                [galaxy.position.row >= ground_row for ground_row in ground_rows]
            )
            columns_to_increment = sum(
                [
                    galaxy.position.column >= ground_column
                    for ground_column in ground_columns
                ]
            )
            galaxy.position.row += rows_to_increment * (multiplier - 1)
            galaxy.position.column += columns_to_increment * (multiplier - 1)

        logger.debug(', '.join([str(galaxy) for galaxy in galaxies.values()]))

        distance = 0
        for i in sorted(galaxies.keys()):
            for j in sorted(galaxies.keys()):
                if j <= i:
                    continue
                distance += galaxies[i].distance(galaxies[j])

        logger.debug(f'Distance: {distance}')

        return distance


if __name__ == '__main__':
    Day11Solver().solve_first_problem("day_11/input.txt")
    Day11Solver().solve_second_problem("day_11/input.txt", 1000000)
