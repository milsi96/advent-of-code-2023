import logging
import sys
from file_reader.file_reader import FileReader
import re


logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


class Map:
    souce_category: str
    destination_category: str
    source_ranges: list[range]
    destination_ranges: list[range]

    def __init__(
        self,
        source_category: str,
        destination_category: str,
        source_ranges: list[range],
        destination_ranges: list[range],
    ):
        self.source_category = source_category
        self.destination_category = destination_category
        self.source_ranges = source_ranges
        self.destination_ranges = destination_ranges

    def get_destination(self, source: int) -> int:
        found = False
        for range_number in range(len(self.source_ranges)):
            if source in self.source_ranges[range_number]:
                difference = source - self.source_ranges[range_number].start
                found = True
                result = self.destination_ranges[range_number].start + difference
                logger.debug(f'Destination for source {source} is {result}')
                return result

        if not found:
            logger.debug(f'Destination for source {source} is {source}')
            return source


class Day5Solver(FileReader):
    DESTINATION_RANGE_START = 0
    SOURCE_RANGE_START = 1
    RANGE_LENGTH = 2

    def _parse_lines(self, lines: list[str]) -> (list[int], dict[str, Map]):
        seeds_pattern = r'^seeds:\s.+$'
        map_pattern = r'^(.+)-to-(.+)\smap:$'
        range_pattern = r'^(\d+)\s(\d+)\s(\d+)$'

        seeds: list[int] = []
        maps: dict[str, Map] = {}
        for i in range(len(lines)):
            if re.match(seeds_pattern, lines[i]):
                seeds.extend(
                    [int(seed) for seed in lines[i].split(':')[1].strip().split(' ')]
                )
                logger.info(f'Seeds found: {seeds}')
            elif re.match(map_pattern, lines[i]):
                source_category, destination_category = re.findall(
                    map_pattern, lines[i]
                )[0]
                logger.info(f'Map found: {source_category} to {destination_category} ')

                source_ranges: list[range] = []
                destination_ranges: list[range] = []
                increment = 1
                while (
                    i + increment < len(lines) is not None
                    and lines[i + increment] != ''
                ):
                    conversion = [
                        int(num)
                        for num in re.findall(range_pattern, lines[i + increment])[0]
                    ]

                    source_ranges.append(
                        range(
                            conversion[self.SOURCE_RANGE_START],
                            conversion[self.SOURCE_RANGE_START]
                            + conversion[self.RANGE_LENGTH],
                        )
                    )

                    destination_ranges.append(
                        range(
                            conversion[self.DESTINATION_RANGE_START],
                            conversion[self.DESTINATION_RANGE_START]
                            + conversion[self.RANGE_LENGTH],
                        )
                    )

                    increment = increment + 1

                logger.debug(f'Source ranges found: {source_ranges}')
                logger.debug(f'Destination ranges found: {destination_ranges}')
                maps[source_category] = Map(
                    source_category,
                    destination_category,
                    source_ranges,
                    destination_ranges,
                )

                i = i + 2
            else:
                continue

        return (seeds, maps)

    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        seeds, maps = self._parse_lines(lines)
        locations: list[int] = []

        for seed in seeds:
            logger.info(f'Calculating location for seed {seed}')
            number = seed
            initial_source = 'seed'
            while initial_source != 'location':
                number = maps[initial_source].get_destination(number)
                initial_source = maps[initial_source].destination_category
            locations.append(number)
            logger.info(f'Location for seed {seed} is {number}')

        result = min(locations)
        logger.info(f'Lowest location is {result}')
        return result


if __name__ == '__main__':
    Day5Solver().solve_first_problem("day_5/input.txt")
    # Day5Solver().solve_second_problem("day_4/input_2.txt")
