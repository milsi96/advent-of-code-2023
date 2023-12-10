from typing import Any, Optional
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver
import copy
from matplotlib import path

logger = CustomLogger(__name__).get_logger()


class Position:
    row: int
    column: int

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def __str__(self) -> str:
        return f'({self.row}, {self.column})'

    def __eq__(self, other: Any):
        if isinstance(other, Position):
            return self.row == other.row and self.column == other.column
        return False


class Move:
    row_increment: int
    column_increment: int

    def __init__(self, row_increment: int, column_increment: int):
        if row_increment not in [-1, 0, 1] or column_increment not in [-1, 0, 1]:
            error = (
                f'({self.row_increment}, {self.column_increment}) is not a valid move'
            )
            logger.error(error)
            raise ValueError(error)

        self.row_increment = row_increment
        self.column_increment = column_increment

    def __str__(self) -> str:
        match self.row_increment, self.column_increment:
            case (-1, 0):
                return 'UP'
            case (1, 0):
                return 'DOWN'
            case (0, -1):
                return 'LEFT'
            case (0, 1):
                return 'RIGHT'
            case _:
                return ''


class Tile:
    symbol: str
    position: Position
    moves: list[Move]

    def __init__(self, symbol: str, position: Position):
        self.position = position
        self.symbol = symbol
        self.moves = MoveFactory().get_moves(self.symbol)

    def __str__(self) -> str:
        moves_str = {",".join([str(move) for move in self.moves])}
        return f'{self.position} -> {self.symbol}, moves [{moves_str}]'


class MoveFactory:
    def get_moves(self, symbol: str) -> list[Move]:
        UP = Move(-1, 0)
        DOWN = Move(1, 0)
        LEFT = Move(0, -1)
        RIGHT = Move(0, 1)

        match symbol:
            case '|':
                return [UP, DOWN]
            case '-':
                return [LEFT, RIGHT]
            case 'L':
                return [UP, RIGHT]
            case 'J':
                return [UP, LEFT]
            case '7':
                return [DOWN, LEFT]
            case 'F':
                return [DOWN, RIGHT]
            case 'S':
                return [UP, DOWN, LEFT, RIGHT]
            case _:
                logger.warning(f'No moves found for symbol {symbol}')
                return []


class Grid:
    tiles: list[Tile]
    _start: Optional[Tile] = None

    def __init__(self, tiles: list[Tile]):
        self.tiles = tiles

    def __str__(self) -> str:
        return ','.join([str(tile) for tile in self.tiles])

    @property
    def start(cls) -> Tile:
        if cls._start is not None:
            return cls._start

        for tile in cls.tiles:
            if tile.symbol == 'S':
                logger.debug(f'Found start at {tile.position}')
                cls._start = tile
                return tile

        error = 'No starting tile found'
        logger.error(error)
        raise ValueError(error)

    def get_tile(self, position: Position) -> Optional[Tile]:
        for tile in self.tiles:
            if (
                tile.position.row == position.row
                and tile.position.column == position.column
            ):
                return tile

        warning = f'No tile found at {position}'
        logger.warning(warning)
        return None


class Day10Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        grid = Grid(self.parse_lines(lines))

        logger.info(f'Starting Position: {grid.start}')
        possible_loop_starts: list[Tile] = []
        for next_move in grid.start.moves:
            next_position = Position(
                grid.start.position.row + next_move.row_increment,
                grid.start.position.column + next_move.column_increment,
            )
            next_tile = grid.get_tile(next_position)
            if next_tile is not None:
                possible_loop_starts.append(next_tile)

        loop_start: Tile
        for tile in possible_loop_starts:
            for move in tile.moves:
                next_position = Position(
                    tile.position.row + move.row_increment,
                    tile.position.column + move.column_increment,
                )
                next_tile = grid.get_tile(next_position)
                if next_tile is not None and next_tile.symbol == 'S':
                    loop_start = tile

        prev_pos = Position(grid.start.position.row, grid.start.position.column)
        current_pos = Position(loop_start.position.row, loop_start.position.column)

        steps = 1
        while current_pos != grid.start.position:
            steps += 1
            current_tile = grid.get_tile(current_pos)
            if current_tile is None:
                raise ValueError(f'No tile at position {current_pos}')
            possible_moves = current_tile.moves
            logger.debug(f'Current tile: {current_tile}')
            for move in possible_moves:
                next_position = Position(
                    current_tile.position.row + move.row_increment,
                    current_tile.position.column + move.column_increment,
                )
                next_tile = grid.get_tile(next_position)
                if next_tile is None:
                    error = f'No next tile found at {next_position}'
                    logger.error(error)
                    continue
                if next_tile.position != prev_pos:
                    prev_pos = copy.copy(current_tile.position)
                    current_pos = copy.deepcopy(next_tile.position)
                    break

        result = int(steps / 2)
        logger.info(f'Total steps {result}')

        return result

    def parse_lines(self, lines: list[str]) -> list[Tile]:
        tiles: list[Tile] = []

        for row in range(len(lines)):
            for column in range(len(lines[row])):
                if lines[row][column] != '.':
                    tiles.append(Tile(lines[row][column], Position(row, column)))

        return tiles

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        grid = Grid(self.parse_lines(lines))

        logger.info(f'Starting Position: {grid.start}')

        possible_loop_starts: list[Tile] = []
        for next_move in grid.start.moves:
            next_position = Position(
                grid.start.position.row + next_move.row_increment,
                grid.start.position.column + next_move.column_increment,
            )
            next_tile = grid.get_tile(next_position)
            if next_tile is not None:
                possible_loop_starts.append(next_tile)

        loop_start: Tile
        for tile in possible_loop_starts:
            for move in tile.moves:
                next_position = Position(
                    tile.position.row + move.row_increment,
                    tile.position.column + move.column_increment,
                )
                next_tile = grid.get_tile(next_position)
                if next_tile is not None and next_tile.symbol == 'S':
                    loop_start = tile

        prev_pos = Position(grid.start.position.row, grid.start.position.column)
        current_pos = Position(loop_start.position.row, loop_start.position.column)

        positions: list[Position] = [prev_pos, current_pos]
        while current_pos != grid.start.position:
            current_tile = grid.get_tile(current_pos)
            if current_tile is None:
                raise ValueError(f'No tile at position {current_pos}')
            possible_moves = current_tile.moves
            logger.debug(f'Current tile: {current_tile}')
            for move in possible_moves:
                next_position = Position(
                    current_tile.position.row + move.row_increment,
                    current_tile.position.column + move.column_increment,
                )
                next_tile = grid.get_tile(next_position)
                if next_tile is None:
                    error = f'No next tile found at {next_position}'
                    logger.error(error)
                    continue
                if next_tile.position != prev_pos:
                    prev_pos = copy.copy(current_tile.position)
                    current_pos = copy.deepcopy(next_tile.position)
                    positions.append(current_pos)
                    break

        logger.debug(', '.join([str(pos) for pos in positions]))

        loop_tuple = [(pos.row, pos.column) for pos in positions]
        loop = path.Path(loop_tuple)
        logger.debug(loop.contains_point((6, 4)))
        grounds: list[Position] = self.get_grounds(lines)

        grid_tiles_tuple = [
            (tile.position.row, tile.position.column) for tile in grid.tiles
        ]
        to_check = [(pos.row, pos.column) for pos in grounds]
        enclosed_tiles = 0
        for pos in to_check + grid_tiles_tuple:
            if pos in loop_tuple:
                continue
            if loop.contains_point(pos):
                logger.debug(f'Tile {pos} is enclosed by the loop')
                enclosed_tiles += 1

        logger.info(f'The total of enclosed tiles is {enclosed_tiles}')

        return enclosed_tiles

    def get_grounds(self, lines: list[str]) -> list[Position]:
        result: list[Position] = []

        for row in range(len(lines)):
            for column in range(len(lines[row])):
                if lines[row][column] == '.':
                    result.append(Position(row, column))

        return result


if __name__ == '__main__':
    # Day10Solver().solve_first_problem("day_10/input.txt")
    Day10Solver().solve_second_problem("day_10/input.txt")
