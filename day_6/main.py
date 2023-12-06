from custom_logger.custom_logger import CustomLogger
from file_reader.file_reader import FileReader


logger = CustomLogger(__name__).get_logger()


class Day6Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        times = self.parse_line(lines[0])
        distances = self.parse_line(lines[1])
        logger.info(f'Times found: {times}')
        logger.info(f'Distances found: {distances}')

        result = 1
        for i in range(len(times)):
            result = result * self.get_winning_times(times[i], distances[i])

        logger.info(f'The record can be beaten in {result} different ways')
        return result

    def parse_line(self, line: str) -> list[int]:
        return [int(num) for num in line.split(':')[1].strip().split(' ') if num != '']

    def get_winning_times(self, time: int, target_distance: int) -> int:
        result: int = 0
        upper_limit = 0
        if time % 2 == 0:
            upper_limit = (time / 2) + 1
        else:
            upper_limit = (time + 1) / 2

        for i in range(int((upper_limit)) - 1, 0, -1):
            distance = i * (time - i)
            if distance > target_distance:
                logger.debug(
                    f'Pressing the button for {i} milliseconds '
                    f'will result in a {distance} millimeters distance'
                )
                result = result + 1
            else:
                break
        if time % 2 == 0:
            result = result * 2 - 1
        else:
            result = result * 2
        return result

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        times = self.parse_line(lines[0])
        distances = self.parse_line(lines[1])

        target_time = int(''.join([str(num) for num in times]))
        target_distance = int(''.join([str(num) for num in distances]))
        logger.info(f'Taget time found: {target_time}')
        logger.info(f'Target distance found: {target_distance}')

        result = self.get_winning_times(target_time, target_distance)

        logger.info(f'The record can be beaten in {result} different ways')
        return result


if __name__ == '__main__':
    # Day6Solver().solve_first_problem("day_6/input.txt")
    Day6Solver().solve_second_problem("day_6/input.txt")
