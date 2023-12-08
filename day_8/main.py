import math
import re
from custom_logger.custom_logger import CustomLogger
from file_reader.file_reader import FileReader

logger = CustomLogger(__name__).get_logger()


class Node:
    name: str
    left_node: str
    right_node: str

    def __init__(self, name: str, left_node: str, right_node: str):
        self.name = name
        self.left_node = left_node
        self.right_node = right_node

    def __str__(self) -> str:
        return f'{self.name} = ({self.left_node}, {self.right_node})'


class Day8Solver(FileReader):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        instructions = list(lines[0])

        nodes: dict[str, Node] = {}
        for line in lines[2:]:
            node = self.parse_line(line)
            nodes[node.name] = node

        logger.info(f'Instructions: {instructions}')
        for node in nodes.values():
            logger.info(node)

        steps = 0
        current_node = nodes['AAA']
        current_instruction = 0
        while current_node.name != 'ZZZ':
            logger.debug(f'Current node is {current_node.name}')

            if instructions[current_instruction] == 'L':
                current_node = nodes.get(current_node.left_node)
            elif instructions[current_instruction] == 'R':
                current_node = nodes.get(current_node.right_node)

            steps = steps + 1
            if current_instruction == (len(instructions) - 1):
                logger.debug('Restarting instructions')
                current_instruction = 0
            else:
                current_instruction = current_instruction + 1

        logger.info(f'Took {steps} steps to reach ZZZ')
        return steps

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        instructions = list(lines[0])

        nodes: dict[str, Node] = {}
        for line in lines[2:]:
            node = self.parse_line(line)
            nodes[node.name] = node

        logger.info(f'Instructions: {instructions}')
        for node in nodes.values():
            logger.info(node)

        starting_nodes = [node for node in nodes.values() if node.name.endswith('A')]

        total_steps: dict[str, int] = {}
        for node in starting_nodes:
            current_instruction = 0
            steps = 0
            current_node = node
            while not current_node.name.endswith('Z'):
                logger.debug(f'Current node is {current_node.name}')

                if instructions[current_instruction] == 'L':
                    current_node = nodes.get(current_node.left_node)
                elif instructions[current_instruction] == 'R':
                    current_node = nodes.get(current_node.right_node)

                steps = steps + 1
                if current_instruction == (len(instructions) - 1):
                    logger.debug('Restarting instructions')
                    current_instruction = 0
                else:
                    current_instruction = current_instruction + 1

            total_steps[node.name] = steps

        result = math.lcm(*total_steps.values())
        logger.info(f'Took {result} steps to reach ZZZ')
        return result

    def parse_line(self, line: str) -> Node:
        node_pattern = r'^(.{3})\s=\s\((.{3}),\s(.{3})\)$'
        NAME = 0
        LEFT_NODE = 1
        RIGHT_NODE = 2
        matches = re.match(node_pattern, line).groups()
        return Node(matches[NAME], matches[LEFT_NODE], matches[RIGHT_NODE])


if __name__ == '__main__':
    # Day8Solver().solve_first_problem("day_8/input.txt")
    Day8Solver().solve_second_problem("day_8/input.txt")
