
from typing import List
from util import get_input


def sonar_sweep(input: List[int], window: int = 1) -> int:
    return sum(curr > prev for prev, curr in zip(input, input[window:]))


if __name__ == '__main__':
    input = [int(n) for n in get_input(year=2021, day=1)]

    print(f'Part 1 answer: {sonar_sweep(input, window=1)}')
    print(f'Part 2 answer: {sonar_sweep(input, window=3)}')
