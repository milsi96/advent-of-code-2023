from enum import StrEnum
import math
from typing import Optional
from custom_logger.custom_logger import CustomLogger
from solver.solver import Solver
import re


logger = CustomLogger(__name__).get_logger()


class ModuleType(StrEnum):
    BROADCASTER = 'broadcaster'
    FLIP_FLOP = '%'
    CONJUNCTION = '&'


class Module:
    name: str
    current_pulse: bool
    destinations: list[str]
    type: Optional[ModuleType]

    def __init__(
        self,
        name: str,
        current_pulse: bool,
        destinations: list[str],
        type: Optional[ModuleType] = None,
    ) -> None:
        self.name = name
        self.current_pulse = current_pulse
        self.destinations = destinations
        self.type = type

    def __str__(self) -> str:
        return f'{self.name} is set to {"high" if self.current_pulse else "low"}'

    @property
    def out_voltage(self) -> bool:
        match self.type:
            case ModuleType.BROADCASTER:
                return False
            case ModuleType.FLIP_FLOP:
                return self.current_pulse
            case ModuleType.CONJUNCTION:
                return not self.current_pulse
            case _:
                raise ValueError(f'Untyped module {self.name} cannot send pulses!')


class Pulse:
    source: str
    voltage: bool
    destination: str

    def __init__(self, source: str, voltage: bool, destination: str) -> None:
        self.source = source
        self.voltage = voltage
        self.destination = destination

    def __str__(self) -> str:
        return (
            f'{self.source} -{"high" if self.voltage else "low"}-> {self.destination}'
        )


class Day20Solver(Solver):
    def solve_first_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        modules: dict[str, Module] = {}

        for line in lines:
            pattern = r'^(.+)\s->\s(.+)$'
            source, signals = re.findall(pattern, line)[0]
            if source == ModuleType.BROADCASTER:
                modules[source] = Module(
                    source, False, signals.split(', '), ModuleType.BROADCASTER
                )
            elif source[0] == ModuleType.FLIP_FLOP:
                modules[source[1:]] = Module(
                    source[1:], False, signals.split(', '), ModuleType.FLIP_FLOP
                )
            elif source[0] == ModuleType.CONJUNCTION:
                modules[source[1:]] = Module(
                    source[1:], False, signals.split(', '), ModuleType.CONJUNCTION
                )

        logger.debug(", ".join(map(str, modules.values())))

        previous_inputs: dict[str, dict[str, bool]] = {}
        for conj in [
            mod.name for mod in modules.values() if mod.type == ModuleType.CONJUNCTION
        ]:
            temp: dict[str, bool] = {}
            for input in self.conjunction_input_modules(conj, modules):
                temp[input] = False
            previous_inputs[conj] = temp

        MAX = 1000
        result: dict[bool, int] = {}
        for i in range(0, MAX):
            logger.debug(f' ***  CYCLE {i+1}  *** ')
            self.push_button(modules, previous_inputs, result)

        logger.debug(
            f'Result is {result} and the total is {result[True] * result[False]}'
        )

        return result[True] * result[False]

    def push_button(
        self,
        modules: dict[str, Module],
        previous_inputs: dict[str, dict[str, bool]],
        pulses_sent: dict[bool, int] = {},
    ) -> dict[bool, int]:
        broadcaster = modules[ModuleType.BROADCASTER]
        pulses_sent[False] = pulses_sent.get(False, 0) + 1
        pulses: list[Pulse] = [
            Pulse(broadcaster.name, broadcaster.out_voltage, signal)
            for signal in broadcaster.destinations
        ]

        def XNOR(a: bool, b: bool):
            if a == b:
                return True
            else:
                return False

        while len(pulses) > 0:
            # logger.debug(", ".join(map(str, modules.values())))
            current_pulse = pulses.pop(0)
            pulses_sent[current_pulse.voltage] = (
                pulses_sent.get(current_pulse.voltage, 0) + 1
            )
            current_pulse.voltage = modules[current_pulse.source].out_voltage
            if current_pulse.destination not in modules:
                if current_pulse.destination == 'rx' and not current_pulse.voltage:
                    return {True: -1, False: -1}
                continue
            dest_module = modules[current_pulse.destination]
            match dest_module.type:
                case ModuleType.FLIP_FLOP:
                    if not current_pulse.voltage:
                        dest_module.current_pulse = XNOR(
                            dest_module.current_pulse, current_pulse.voltage
                        )
                        for dest in dest_module.destinations:
                            pulses.append(
                                Pulse(dest_module.name, dest_module.current_pulse, dest)
                            )
                case ModuleType.CONJUNCTION:
                    previous_inputs[dest_module.name][
                        current_pulse.source
                    ] = current_pulse.voltage
                    if all(previous_inputs[dest_module.name].values()):
                        dest_module.current_pulse = True
                    else:
                        dest_module.current_pulse = False
                    for dest in dest_module.destinations:
                        pulses.append(
                            Pulse(dest_module.name, not dest_module.current_pulse, dest)
                        )

        for mod in modules.values():
            if mod.type == ModuleType.CONJUNCTION:
                mod.current_pulse = False

        return pulses_sent

    def conjunction_input_modules(
        self, conjuction: str, modules: dict[str, Module]
    ) -> list[str]:
        result: list[str] = []
        for module in modules.values():
            if conjuction in module.destinations:
                result.append(module.name)
        return result

    def solve_second_problem(self, file_name: str) -> int:
        lines = self.get_lines(file_name)
        modules: dict[str, Module] = {}

        for line in lines:
            pattern = r'^(.+)\s->\s(.+)$'
            source, signals = re.findall(pattern, line)[0]
            if source == ModuleType.BROADCASTER:
                modules[source] = Module(
                    source, False, signals.split(', '), ModuleType.BROADCASTER
                )
            elif source[0] == ModuleType.FLIP_FLOP:
                modules[source[1:]] = Module(
                    source[1:], False, signals.split(', '), ModuleType.FLIP_FLOP
                )
            elif source[0] == ModuleType.CONJUNCTION:
                modules[source[1:]] = Module(
                    source[1:], False, signals.split(', '), ModuleType.CONJUNCTION
                )

        logger.debug(", ".join(map(str, modules.values())))

        previous_inputs: dict[str, dict[str, bool]] = {}
        for conj in [
            mod.name for mod in modules.values() if mod.type == ModuleType.CONJUNCTION
        ]:
            temp: dict[str, bool] = {}
            for input in self.conjunction_input_modules(conj, modules):
                temp[input] = False
            previous_inputs[conj] = temp

        true_inputs: dict[str, int] = {}
        result: dict[bool, int] = {}
        for input in ['vg', 'gs', 'kd', 'zf']:
            i = 0
            while not modules[input].current_pulse:
                logger.debug(f' ***  CYCLE {input}-{i+1}  *** ')
                result = self.push_button(modules, previous_inputs, result)
                logger.debug(
                    ", ".join(
                        [f'{mod.name}: {mod.current_pulse}' for mod in modules.values()]
                    )
                )
                i += 1
                break
            true_inputs[input] = i
            for mod in modules.values():
                mod.current_pulse = False

        logger.debug(
            'The machine rx received a low pulse, took {} button presses'.format(
                math.lcm(*true_inputs.values())
            )
        )

        return i + 1


if __name__ == '__main__':
    Day20Solver().solve_first_problem("day_20/input.txt")
    Day20Solver().solve_second_problem("day_20/input.txt")
