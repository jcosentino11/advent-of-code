from typing import List
from util import get_input


def calculate_min_alignment_fuel(crab_positions: List[int]) -> int:
    min_position = min(crab_positions)
    max_position = max(crab_positions)

    min_fuel_cost = (max_position - min_position) * len(crab_positions)

    for alignment_position in range(min_position, max_position + 1):
        fuel_cost = 0
        for position in crab_positions:
            fuel_cost += abs(alignment_position - position)
            if fuel_cost > min_fuel_cost:
                break

        if fuel_cost < min_fuel_cost:
            min_fuel_cost = fuel_cost

    return min_fuel_cost


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=7)
    crab_positions = [int(position) for position in raw_input[0].split(",")]

    print(
        f'Part 1 answer: {calculate_min_alignment_fuel(crab_positions)}')
