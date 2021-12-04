
from __future__ import annotations
from typing import List
from util import get_input
from dataclasses import dataclass


@dataclass
class Command:
    direction: str
    magnitude: int

    @staticmethod
    def from_input(input: str) -> Command:
        direction, magnitude = input.split(' ')
        return Command(direction, int(magnitude))


def dive(commands: List[Command]) -> int:
    horizontal_position = 0
    depth = 0

    for command in commands:
        if command.direction == 'forward':
            horizontal_position += command.magnitude
        elif command.direction == 'up':
            depth -= command.magnitude
        elif command.direction == 'down':
            depth += command.magnitude

    return horizontal_position * depth


def dive_with_aim(commands: List[Command]) -> int:
    horizontal_position = 0
    depth = 0
    aim = 0

    for command in commands:
        if command.direction == 'forward':
            horizontal_position += command.magnitude
            depth += aim * command.magnitude
        elif command.direction == 'up':
            aim -= command.magnitude
        elif command.direction == 'down':
            aim += command.magnitude

    return horizontal_position * depth


if __name__ == '__main__':
    input = get_input(year=2021, day=2)
    commands = list(map(Command.from_input, input))

    print(f'Part 1 answer: {dive(commands)}')
    print(f'Part 2 answer: {dive_with_aim(commands)}')
