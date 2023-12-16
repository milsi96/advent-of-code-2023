from enum import IntEnum, StrEnum
from typing import Optional
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver

logger = CustomLogger(__name__).get_logger()


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class TileValue(StrEnum):
    EMPTY_SPACE = '.'
    MIRROR_45 = '\\'
    MIRROR_135 = '/'
    VERTICAL_SPLITTER = '|'
    HORIZONTAL_SPLITTER = '-'


class Tile:
    row: int
    column: int
    tile_value: TileValue

    def __init__(self, row: int, column: int, tile_value: TileValue) -> None:
        self.row = row
        self.column = column
        self.tile_value = tile_value

    def __str__(self) -> str:
        return f'{self.tile_value} ({self.row}, {self.column})'

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Tile):
            return False
        return (
            self.row == __value.row
            and self.column == __value.column
            and self.tile_value == __value.tile_value
        )

    def __hash__(self) -> int:
        return self.row * self.column * ord(self.tile_value.value)


class Move:
    direction: Direction
    next_tile: Tile

    def __init__(self, direction: Direction, next_tile: Tile) -> None:
        self.direction = direction
        self.next_tile = next_tile

    def __str__(self) -> str:
        return f'{self.next_tile} from {self.direction.name}'

    def __hash__(self) -> int:
        return (
            self.next_tile.row
            * self.next_tile.column
            * ord(self.next_tile.tile_value.value)
            * self.direction.value
        )

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Move):
            return False
        return (
            self.next_tile == __value.next_tile and self.direction == __value.direction
        )


class Day16Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        contraption = self.parse_contraption(self.get_lines(file_name))

        seen_moves: set[Move] = set()

        self.print_contraption(contraption)

        next_moves: list[Move] = [Move(Direction.RIGHT, contraption[0][0])]
        while len(next_moves) != 0:
            move = next_moves.pop(0)
            if move in seen_moves:
                continue
            seen_moves.add(move)
            logger.debug(
                f'Moving from tile {move.next_tile} in direction {move.direction.name}'
            )
            temp_moves = self.next_tiles(contraption, move.direction, move.next_tile)
            if temp_moves is not None:
                next_moves.extend(temp_moves)

        seen_tiles: set[Tile] = {move.next_tile for move in seen_moves}
        energized_tiles = len(seen_tiles)
        logger.debug(f'Energized tiles are {energized_tiles}')

        return energized_tiles

    def print_contraption(self, contraption: list[list[Tile]]) -> None:
        for line in contraption:
            logger.debug(' '.join([str(tile) for tile in line]))

    def parse_contraption(self, lines: list[str]) -> list[list[Tile]]:
        result: list[list[Tile]] = []
        for row in range(len(lines)):
            temp: list[Tile] = []
            for column in range(len(lines[row])):
                temp.append(Tile(row, column, TileValue(lines[row][column])))
            result.append(temp)
        return result

    def next_tiles(
        self, contraption: list[list[Tile]], direction: Direction, current_tile: Tile
    ) -> Optional[list[Move]]:
        match current_tile.tile_value:
            case TileValue.EMPTY_SPACE:
                next_move = self.move_from_empty_tile(
                    contraption, direction, current_tile
                )
                if next_move is None:
                    return None
                return [next_move]
            case TileValue.MIRROR_45:
                next_move = self.move_from_mirror_45(
                    contraption, direction, current_tile
                )
                if next_move is None:
                    return None
                return [next_move]
            case TileValue.MIRROR_135:
                next_move = self.move_from_mirror_135(
                    contraption, direction, current_tile
                )
                if next_move is None:
                    return None
                return [next_move]
            case TileValue.VERTICAL_SPLITTER:
                return self.move_from_vertical_splitter(
                    contraption, direction, current_tile
                )
            case TileValue.HORIZONTAL_SPLITTER:
                return self.move_from_horizontal_splitter(
                    contraption, direction, current_tile
                )
            case _:
                return None

    def move_from_horizontal_splitter(
        self, contraption: list[list[Tile]], direction: Direction, current_tile: Tile
    ) -> Optional[list[Move]]:
        ## This is HORIZONTAL_SPLITTER: '-'
        result: list[Move] = []
        match direction:
            case Direction.UP | Direction.DOWN:
                move_left = self.move_from_empty_tile(
                    contraption, Direction.LEFT, current_tile
                )
                move_right = self.move_from_empty_tile(
                    contraption, Direction.RIGHT, current_tile
                )
                if move_left is not None:
                    result.append(move_left)
                if move_right is not None:
                    result.append(move_right)
            case Direction.LEFT | Direction.RIGHT:
                move = self.move_from_empty_tile(contraption, direction, current_tile)
                if move is not None:
                    result.append(move)
        if len(result) == 0:
            return None
        return result

    def move_from_vertical_splitter(
        self, contraption: list[list[Tile]], direction: Direction, current_tile: Tile
    ) -> Optional[list[Move]]:
        ## This is VERTICAL_SPLITTER: '|'
        result: list[Move] = []
        match direction:
            case Direction.RIGHT | Direction.LEFT:
                move_up = self.move_from_empty_tile(
                    contraption, Direction.UP, current_tile
                )
                move_down = self.move_from_empty_tile(
                    contraption, Direction.DOWN, current_tile
                )
                if move_up is not None:
                    result.append(move_up)
                if move_down is not None:
                    result.append(move_down)
            case Direction.UP | Direction.DOWN:
                move = self.move_from_empty_tile(contraption, direction, current_tile)
                if move is not None:
                    result.append(move)
        if len(result) == 0:
            return None
        return result

    def move_from_mirror_135(
        self, contraption: list[list[Tile]], direction: Direction, current_tile: Tile
    ) -> Optional[Move]:
        ## This is MIRROR_135: '/'
        match direction:
            case Direction.RIGHT:
                return self.move_from_empty_tile(
                    contraption, Direction.UP, current_tile
                )
            case Direction.LEFT:
                return self.move_from_empty_tile(
                    contraption, Direction.DOWN, current_tile
                )
            case Direction.UP:
                return self.move_from_empty_tile(
                    contraption, Direction.RIGHT, current_tile
                )
            case Direction.DOWN:
                return self.move_from_empty_tile(
                    contraption, Direction.LEFT, current_tile
                )

    def move_from_mirror_45(
        self, contraption: list[list[Tile]], direction: Direction, current_tile: Tile
    ) -> Optional[Move]:
        ## This is MIRROR_45: '\'
        match direction:
            case Direction.RIGHT:
                return self.move_from_empty_tile(
                    contraption, Direction.DOWN, current_tile
                )
            case Direction.LEFT:
                return self.move_from_empty_tile(
                    contraption, Direction.UP, current_tile
                )
            case Direction.UP:
                return self.move_from_empty_tile(
                    contraption, Direction.LEFT, current_tile
                )
            case Direction.DOWN:
                return self.move_from_empty_tile(
                    contraption, Direction.RIGHT, current_tile
                )

    def move_from_empty_tile(
        self, contraption: list[list[Tile]], direction: Direction, current_tile: Tile
    ) -> Optional[Move]:
        match direction:
            case Direction.UP:
                if current_tile.row - 1 < 0:
                    return None
                return Move(
                    direction, (contraption[current_tile.row - 1][current_tile.column])
                )
            case Direction.RIGHT:
                if current_tile.column + 1 >= len(contraption[current_tile.row]):
                    return None
                return Move(
                    direction, contraption[current_tile.row][current_tile.column + 1]
                )
            case Direction.DOWN:
                if current_tile.row + 1 >= len(contraption):
                    return None
                return Move(
                    direction, contraption[current_tile.row + 1][current_tile.column]
                )
            case Direction.LEFT:
                if current_tile.column - 1 < 0:
                    return None
                return Move(
                    direction, contraption[current_tile.row][current_tile.column - 1]
                )

    def solve_second_problem(self, file_name: str) -> int:
        return 0


if __name__ == '__main__':
    Day16Solver().solve_first_problem("day_16/input.txt")
    Day16Solver().solve_second_problem("day_16/input.txt")
