from typing import Callable, List
from util import get_input


def calculate_min_fuel(
        positions: List[int],
        cost: Callable[[int], int] = lambda x: x) -> int:
    """
    Calculate the minimum amount of fuel needed to align all the crabs.

    Parameters
    ----------
    positions: List[int]
        List of horizontal crab positions
    cost: Callable[[int], int]
        Function that computes cost, given number of horizontal crab moves as input.
        By default, cost is equal to number of crab moves.
    """

    def alignment_cost(target_pos: int) -> int:
        return sum([cost(abs(target_pos - position)) for position in positions])

    return min([alignment_cost(position) for position in range(min(positions), max(positions) + 1)])


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=7)
    positions = [int(position) for position in raw_input[0].split(",")]

    def increasing_cost(steps: int) -> int:
        """
        Given a total number of crab steps, calculate the cost.
        Cost increases by 1 for each crab, with initial cost being 1.

        Essentially, this function just sums integers from 1 to steps, inclusive.

        Parameters
        ----------
        steps: int
            number of crab steps

        Examples
        --------

        increasing_cost(1) == 1
        increasing_cost(2) == 3
        increasing_cost(3) == 6

        """
        return int(steps * (steps + 1) / 2)

    print(
        f'Part 1 answer: {calculate_min_fuel(positions)}')
    print(
        f'Part 2 answer: {calculate_min_fuel(positions, cost=increasing_cost)}')
