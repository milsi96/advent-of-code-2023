from collections import defaultdict
import re
from typing import Optional
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver


logger = CustomLogger(__name__).get_logger()


class Lens:
    label: str
    focal_length: int

    def __init__(self, label: str, focal_length: int) -> None:
        self.label = label
        self.focal_length = focal_length

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, Lens):
            return False
        return self.label == __value.label

    def __str__(self) -> str:
        return f'[{self.label} {self.focal_length}]'


class Day15Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        tokens = self.get_lines(file_name)[0].split(',')

        result = 0
        for token in tokens:
            result += self.calculate_hash(token)

        logger.debug(f'The sum of the hash conversion is {result}')
        return result

    def calculate_hash(self, token: str) -> int:
        current_value = 0
        for tk in token:
            current_value += ord(tk)
            current_value *= 17
            current_value %= 256
        return current_value

    def solve_second_problem(self, file_name: str) -> int:
        tokens = self.get_lines(file_name)[0].split(',')
        boxes: dict[int, list[Lens]] = defaultdict(lambda: [])

        token_pattern = r'^(\D+)(=|-)(\d)*$'
        for token in tokens:
            label, operation, focal_length_opt = [
                res for res in re.split(token_pattern, token) if res != ''
            ]
            box_num = self.calculate_hash(label)

            focal_length = 0
            if focal_length_opt is not None:
                focal_length = int(focal_length_opt)

            logger.debug(f'Token [{label} {operation} {focal_length}] = {box_num}')
            lens = Lens(label, int(focal_length))

            match operation:
                case '=':
                    index = self.lens_index(boxes[box_num], lens)
                    if index is not None:
                        boxes[box_num].pop(index)
                        boxes[box_num].insert(index, lens)
                    else:
                        boxes[box_num].append(lens)
                case '-':
                    index = self.lens_index(boxes[box_num], lens)
                    if index is not None:
                        boxes[box_num].pop(index)

        focusing_power = 0
        for box, lenses in boxes.items():
            if len(lenses) == 0:
                continue
            logger.debug(f'Box {box}: {" ".join([str(lens) for lens in lenses])}')
            for i in range(len(lenses)):
                focusing_power += (1 + box) * (i + 1) * lenses[i].focal_length

        logger.debug(f'The focusing power is {focusing_power}')
        return 0

    def lens_index(self, lenses: list[Lens], target: Lens) -> Optional[int]:
        for i in range(len(lenses)):
            if lenses[i] == target:
                return i
        return None


if __name__ == '__main__':
    Day15Solver().solve_first_problem("day_15/input.txt")
    Day15Solver().solve_second_problem("day_15/input.txt")
