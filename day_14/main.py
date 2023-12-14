from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver


logger = CustomLogger(__name__).get_logger()


class Day14Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        platform: list[list[str]] = []

        for row in range(len(lines)):
            temp_line: list[str] = []
            for column in range(len(lines[row])):
                temp_line.append(lines[row][column])

            platform.append(temp_line)

        platform = self.tilt_left(platform)
        # platform = self.tilt_left(platform)

        for line in platform:
            logger.debug(line)

        rocks_count = self.count_rocks(platform)
        logger.debug(f'Total rocks after tilting is {rocks_count}')
        return rocks_count

    def tilt_left(self, platform: list[list[str]]) -> list[list[str]]:
        platform = self.transpose(platform)
        for line in platform:
            for index in range(len(line)):
                if line[index] != 'O':
                    continue
                new_index = self.move_rock(line, index)
                if index != new_index:
                    line[new_index] = line[index]
                    line[index] = '.'
        return self.transpose(platform)

    def transpose(self, platform: list[list[str]]) -> list[list[str]]:
        return [
            [platform[j][i] for j in range(len(platform))]
            for i in range(len(platform[0]))
        ]

    def count_rocks(self, platform: list[list[str]]) -> int:
        result = 0
        length = len(platform[0])
        for line in platform:
            result += length * line.count('O')
            length -= 1
        return result

    def move_rock(self, line: list[str], rock_index: int) -> int:
        diff = 0
        while rock_index - diff > 0 and line[rock_index - diff - 1] not in ['O', '#']:
            diff += 1
        return rock_index - diff

    def solve_second_problem(self, file_name: str) -> int:
        # lines = self.get_lines(file_name)

        return 0


if __name__ == '__main__':
    Day14Solver().solve_first_problem("day_14/input.txt")
    # Day14Solver().solve_second_problem("day_14/input.txt")
