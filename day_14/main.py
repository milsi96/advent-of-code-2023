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

        platform = self.tilt_west(self.transpose(platform))
        platform = self.transpose(platform)

        rocks_count = self.count_rocks(platform)
        logger.debug(f'Total rocks after tilting is {rocks_count}')
        return rocks_count

    def tilt_west(self, platform: list[list[str]]) -> list[list[str]]:
        for line in platform:
            for index in range(len(line)):
                if line[index] != 'O':
                    continue
                new_index = self.move_rock_left(line, index)
                if index != new_index:
                    line[new_index] = line[index]
                    line[index] = '.'
        return platform

    def tilt_east(self, platform: list[list[str]]) -> list[list[str]]:
        for line in platform:
            for index in range(len(line) - 1, -1, -1):
                if line[index] != 'O':
                    continue
                new_index = self.move_rock_right(line, index)
                if index != new_index:
                    line[new_index] = line[index]
                    line[index] = '.'
        return platform

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

    def move_rock_left(self, line: list[str], rock_index: int) -> int:
        diff = 0
        while rock_index - diff > 0 and line[rock_index - diff - 1] not in ['O', '#']:
            diff += 1
        return rock_index - diff

    def move_rock_right(self, line: list[str], rock_index: int) -> int:
        diff = 0
        while rock_index + diff + 1 < len(line) and line[rock_index + diff + 1] not in [
            'O',
            '#',
        ]:
            diff += 1
        return rock_index + diff

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        platform: list[list[str]] = []

        for row in range(len(lines)):
            temp_line: list[str] = []
            for column in range(len(lines[row])):
                temp_line.append(lines[row][column])

            platform.append(temp_line)

        logger.debug('')
        MAX_CYCLES = 1000000000

        seen_platforms: dict[int, list[list[str]]] = {}
        repeted_index = 0
        interval_length = 0
        for i in range(MAX_CYCLES):
            platform = self.tilt_north(platform)
            platform = self.tilt_west(platform)
            platform = self.tilt_south(platform)
            platform = self.tilt_east(platform)

            for seen_index in seen_platforms.keys():
                if seen_platforms[seen_index] == platform:
                    repeted_index = seen_index
                    interval_length = i - seen_index
                    break

            if repeted_index != 0:
                break

            seen_platforms[i] = platform
            logger.info(f'At cycle {i} rocks count is {self.count_rocks(platform)}')

        logger.debug(
            f'Start of repetition is {repeted_index} '
            + f'and interval length is {interval_length}'
        )

        billionth_index = (MAX_CYCLES - repeted_index) % interval_length
        rocks_count = self.count_rocks(
            seen_platforms[repeted_index + interval_length - billionth_index]
        )
        logger.info(f'The total after {MAX_CYCLES} cycles is {rocks_count}')
        return rocks_count

    def tilt_south(self, platform: list[list[str]]) -> list[list[str]]:
        platform = self.tilt_east(self.transpose(platform))
        return self.transpose(platform)

    def tilt_north(self, platform: list[list[str]]) -> list[list[str]]:
        platform = self.tilt_west(self.transpose(platform))
        return self.transpose(platform)


if __name__ == '__main__':
    Day14Solver().solve_first_problem("day_14/input.txt")
    Day14Solver().solve_second_problem("day_14/input.txt")
