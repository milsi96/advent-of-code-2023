from functools import reduce
import logging
import sys
from typing import Optional
from file_reader.file_reader import FileReader


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


class Point:
    row: int
    column: int
    value: str

    def __init__(self, row: int, column: int, value: str):
        if row < 0 or column < 0:
            error = (
                f'Row and column must be positive, got row {row} and column {column}'
            )
            logger.error(error)
            raise ValueError(error)
        self.row = row
        self.column = column
        self.value = value

    @property
    def is_number(cls) -> bool:
        return cls.value.isdigit()

    @property
    def is_symbol(cls) -> bool:
        return not cls.is_number

    def __str__(self) -> str:
        return f'Point ({self.row}, {self.column}): {self.value}'


class Schematic:
    points: list[Point]
    symbols: list[Point] = []
    numbers: list[Point] = []

    def __init__(self, points: list[Point]):
        self.points = points
        for p in points:
            if p.is_symbol:
                self.symbols.append(p)
            elif p.is_number:
                self.numbers.append(p)

    def __str__(self) -> str:
        return '\n'.join([str(p) for p in self.points])

    def get_point(self, row: int, column: int) -> Optional[Point]:
        for p in self.points:
            if p.row == row and p.column == column:
                return p
        logger.debug(f'No point found at row {row} and column {column}')
        return None

    def is_number(self, row: int, column: int) -> True:
        point: Point = self.get_point(row, column)
        if point is not None:
            return point.is_number

    def is_symbol(self, row: int, column: int) -> True:
        return not self.is_number(row, column)

    def get_near_numbers(self, row: int, column: int) -> list[Point]:
        temp: list[Point] = []
        if self.get_point(row, column) is None:
            logger.warning(
                f'The point you want near numbers of does not '
                f'exist for row {row} and column {column}'
            )
            return temp

        if not self.get_point(row, column).is_symbol:
            logger.warning(
                f'The point you want near numbers of is not a symbol, '
                f'got {self.get_point(row, column)}'
            )
            return temp

        UPPER_ROW = row - 1
        LEFT_COLUMN = column - 1
        SAME_COLUMN = column
        SAME_ROW = row
        RIGHT_COLUMN = column + 1
        LOWER_ROW = row + 1

        temp.extend(
            [
                self.get_point(UPPER_ROW, LEFT_COLUMN),
                self.get_point(UPPER_ROW, SAME_COLUMN),
                self.get_point(UPPER_ROW, RIGHT_COLUMN),
                self.get_point(SAME_ROW, LEFT_COLUMN),
                self.get_point(SAME_ROW, RIGHT_COLUMN),
                self.get_point(LOWER_ROW, LEFT_COLUMN),
                self.get_point(LOWER_ROW, SAME_COLUMN),
                self.get_point(LOWER_ROW, RIGHT_COLUMN),
            ]
        )

        result = [point for point in temp if point is not None and point.is_number]

        return result

    def get_whole_number(self, row: int, column: int) -> list[Point]:
        result: list[Point] = []
        if not self.get_point(row, column).is_number:
            error = f'No number found at ({row}, {column})'
            logger.warning(error)
            return result

        result.append(self.get_point(row, column))

        left_number_found = True
        last_column_checked = column
        while left_number_found:
            if (
                self.get_point(row, last_column_checked - 1) is not None
                and self.get_point(row, last_column_checked - 1).is_number
            ):
                result.append(self.get_point(row, last_column_checked - 1))
                last_column_checked = last_column_checked - 1
            else:
                left_number_found = False

        right_number_found = True
        last_column_checked = column
        while right_number_found:
            if (
                self.get_point(row, last_column_checked + 1) is not None
                and self.get_point(row, last_column_checked + 1).is_number
            ):
                result.append(self.get_point(row, last_column_checked + 1))
                last_column_checked = last_column_checked + 1
            else:
                right_number_found = False

        sorted_result = sorted(result, key=lambda point: (point.row, point.column))

        return sorted_result

    def convert_to_number(self, points: list[Point]) -> int:
        temp: str = ''
        for p in points:
            temp += p.value
        return int(temp)


class Day3Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)

        schematic: Schematic = self._get_schematic(lines)

        valid_parts: list[int] = []
        for symbol in schematic.symbols:
            near_numbers = schematic.get_near_numbers(symbol.row, symbol.column)
            points_checked: set[Point] = []
            for num in near_numbers:
                whole_number_list = schematic.get_whole_number(num.row, num.column)
                checked = True
                for n in whole_number_list:
                    if n not in points_checked:
                        checked = False
                if not checked:
                    value = schematic.convert_to_number(whole_number_list)
                    valid_parts.append(value)
                    points_checked.extend(whole_number_list)

        logger.info(f'Valid parts: {valid_parts}')
        sum_valid_parts = sum(valid_parts)
        logger.info(f'Sum of valid parts is {sum_valid_parts}')

        return sum_valid_parts

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)

        schematic: Schematic = self._get_schematic(lines)

        valid_parts: list[int] = []
        for symbol in schematic.symbols:
            if symbol.value != '*':
                continue
            logger.info(f'Searching for symbol {symbol}')
            near_numbers = schematic.get_near_numbers(symbol.row, symbol.column)
            points_checked: set[Point] = []
            to_be_multiplied: list[int] = []
            for num in near_numbers:
                whole_number_list = schematic.get_whole_number(num.row, num.column)
                checked = True
                for n in whole_number_list:
                    if n not in points_checked:
                        checked = False
                if not checked:
                    value = schematic.convert_to_number(whole_number_list)
                    to_be_multiplied.append(value)
                    points_checked.extend(whole_number_list)
            if len(to_be_multiplied) == 2:
                valid_parts.append(reduce(lambda x, y: x * y, to_be_multiplied))

        logger.info(f'Valid parts: {valid_parts}')
        sum_valid_parts = sum(valid_parts)
        logger.info(f'Sum of valid parts is {sum_valid_parts}')

        return sum_valid_parts

    def _get_schematic(self, lines: list[str]) -> Schematic:
        points: list[Point] = []
        for row in range(len(lines)):
            for column in range(len(lines[row])):
                if lines[row][column] != '.':
                    points.append(Point(row, column, lines[row][column]))
        return Schematic(points)


if __name__ == '__main__':
    Day3Solver().solve_first_problem("day_3/input_1.txt")
    Day3Solver().solve_second_problem("day_3/input_2.txt")
