from typing import Optional, TypeAlias
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver
import re


logger = CustomLogger(__name__).get_logger()

Workflow: TypeAlias = str


class Ratings:
    x: int
    m: int
    a: int
    s: int

    def __init__(self, x: int, m: int, a: int, s: int) -> None:
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __str__(self) -> str:
        return f'{(self.x, self.m, self.a, self.s)}'

    def __hash__(self) -> int:
        return (self.x, self.m, self.a, self.s).__hash__()

    @property
    def sum(cls) -> int:
        return cls.x + cls.m + cls.a + cls.s


class Rule:
    part_selector: Optional[str]
    operation: Optional[str]
    target_value: Optional[int]
    next_workflow: str

    def __init__(
        self,
        next_workflow: str,
        part_selector: Optional[str] = None,
        operation: Optional[str] = None,
        target_value: Optional[int] = None,
    ) -> None:
        self.part_selector = part_selector
        self.operation = operation
        self.target_value = target_value
        self.next_workflow = next_workflow

    def __str__(self) -> str:
        return str(
            (self.part_selector, self.operation, self.target_value, self.next_workflow)
        )

    def __hash__(self) -> int:
        return (
            self.part_selector,
            self.operation,
            self.target_value,
            self.next_workflow,
        ).__hash__()


class Day19Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)

        rules_pattern = r'^(.+){(.+)}$'
        rating_pattern = r'^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$'

        ratings_list: list[str] = [
            line for line in lines if re.match(rating_pattern, line)
        ]
        workflows_list: list[str] = [
            line for line in lines if re.match(rules_pattern, line)
        ]

        workflows = self.parse_rules(workflows_list)
        ratings = self.parse_ratings(ratings_list)

        total_sum = 0
        for rating in ratings:
            accepted = self.accepted(rating, workflows)

            if accepted:
                logger.debug(f'Rating {rating} is accepted')
                total_sum += rating.sum

        logger.info(f'Total sum in {total_sum}')

        return total_sum

    def accepted(self, rating: Ratings, workflows: dict[Workflow, list[Rule]]) -> bool:
        current_workflow = 'in'

        while current_workflow not in ['A', 'R']:
            rules = workflows[current_workflow]
            # logger.debug(" ".join(map(str, rules)))
            found = False
            for rule in rules:
                match rule.part_selector:
                    case 'x':
                        if eval(f'{rating.x} {rule.operation} {rule.target_value}'):
                            current_workflow = rule.next_workflow
                            found = True
                            break
                    case 'm':
                        if eval(f'{rating.m} {rule.operation} {rule.target_value}'):
                            current_workflow = rule.next_workflow
                            found = True
                            break
                    case 'a':
                        if eval(f'{rating.a} {rule.operation} {rule.target_value}'):
                            current_workflow = rule.next_workflow
                            found = True
                            break
                    case 's':
                        if eval(f'{rating.s} {rule.operation} {rule.target_value}'):
                            current_workflow = rule.next_workflow
                            found = True
                            break
                    case _:
                        continue
            if not found:
                current_workflow = [
                    rule for rule in rules if rule.part_selector is None
                ][0].next_workflow

        logger.debug(f'Final workflow is {current_workflow}')

        if current_workflow == 'A':
            return True
        return False

    def parse_rules(self, rules: list[str]) -> dict[Workflow, list[Rule]]:
        result: dict[Workflow, list[Rule]] = {}
        rules_pattern = r'^(.+){(.+)}$'
        single_rule_pattern = r'^(.+)(>|<){1}(\d+):(.+)$'

        for rule in rules:
            workflow, rules_str = re.findall(rules_pattern, rule)[0]
            rule_list: list[Rule] = []
            for rule in rules_str.split(','):
                if re.match(single_rule_pattern, rule):
                    part, sign, value, target = re.findall(single_rule_pattern, rule)[0]
                    rule_list.append(
                        Rule(
                            part_selector=part,
                            operation=sign,
                            target_value=int(value),
                            next_workflow=target,
                        )
                    )
                else:
                    rule_list.append(Rule(rule))
            result[workflow] = rule_list
        return result

    def parse_ratings(self, ratings_list: list[str]) -> list[Ratings]:
        rating_pattern = r'^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$'
        result: list[Ratings] = []

        for rating in ratings_list:
            x, m, a, s = re.findall(rating_pattern, rating)[0]
            result.append(Ratings(*[int(value) for value in [x, m, a, s]]))

        return result

    def solve_second_problem(self, file_name: str) -> int:
        # This couldbe solved calculating the combinations
        # of valid values for every rating. Es:
        # if x=[1, 4000] and two rules are x<500:R and x<5456:A,
        # numbers that make the value of x admissable are (500, 5456)
        # and so on for the other ratings.
        # The total number of combinations is this calculation
        # for every rating multiplied together.

        return 0


if __name__ == '__main__':
    Day19Solver().solve_first_problem("day_19/input.txt")
    Day19Solver().solve_second_problem("day_19/input.txt")
