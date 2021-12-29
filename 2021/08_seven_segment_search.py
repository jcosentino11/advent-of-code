from typing import List
from util import get_input
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Display:
    """Rough representation of a seven-segment display"""

    """A list of ten unique signal patterns"""
    signal: List[str]
    """A list of four output numbers"""
    output: List[str]


def frequency_of_unique_digits(displays: List[Display]) -> int:
    """
    Find number of digits in display output that correspond to the 
    numbers 1, 4, 7, and 8.

    Parameters
    ----------
    displays: List[Display]
        list of displays
    """
    unique_output_lengths = [2, 3, 4, 7]
    frequencies = defaultdict(int)

    outputs = [display.output for display in displays]
    for output in outputs:
        for digit in output:
            frequencies[len(digit)] += 1

    return sum([freq for length, freq in frequencies.items() if length in unique_output_lengths])


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=8)

    def display(line: str) -> Display:
        signal, output = line.split(' | ')
        return Display(
            signal=signal.split(' '),
            output=output.split(' ')
        )

    displays = [display(line) for line in raw_input]

    print(
        f'Part 1 answer: {frequency_of_unique_digits(displays)}')
