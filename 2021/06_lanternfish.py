from __future__ import annotations
from typing import List, Optional
from util import get_input


class Lanternfish:

    TIMER_RESET_VALUE = 6

    def __init__(self, timer: int) -> None:
        "current timer value"
        self._timer: int = timer

    def next_day(self) -> Optional[Lanternfish]:
        """
        Simulate the next day in the lanternfish's life.
        If timer reaches zero, a new fish is spawnwed from this one.
        """
        if self._timer == 0:
            self._timer = Lanternfish.TIMER_RESET_VALUE
            return Lanternfish(timer=self._timer + 2)

        self._timer -= 1


class LanternfishSimulation:

    def __init__(self,
                 starting_population: List[Lanternfish],
                 days: int,
                 verbose: bool = False) -> None:
        "Current population of lanternfish"
        self._population: List[Lanternfish] = starting_population
        "Number of days to simulate"
        self._days: int = days
        "Current number of days left in the simulation"
        self._days_left: int = days
        "Whether verbose logging is enabled"
        self._verbose: bool = verbose

    def complete(self) -> bool:
        """
        True if there are no more days left in the simulation
        """
        return self._days_left == 0

    def population_size(self) -> int:
        """
        Returns the size of the current population
        """
        return len(self._population)

    def next_day(self) -> None:
        """
        Run the next day of simulation for the entire population of fish
        """
        self._next_day_naive()

    def _next_day_naive(self) -> None:
        if self.complete():
            return

        new_fish = []

        for fish in self._population:
            spawned_fish = fish.next_day()
            if spawned_fish:
                new_fish.append(spawned_fish)

        self._population.extend(new_fish)
        self._days_left -= 1

        if self._verbose:
            print(
                f'After {self._days - self._days_left} day(s): {",".join([str(fish._timer) for fish in self._population])}')

    def _next_day_optimized(self) -> None:
        # TODO the naive implementation doesn't work for problem 2, come up with a better way
        pass


def get_lanternfish_count(starting_population: List[Lanternfish], days: int) -> int:
    simulation = LanternfishSimulation(
        starting_population=starting_population,
        days=days,
        # verbose=True
    )
    while not simulation.complete():
        simulation.next_day()
    return simulation.population_size()


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=6)
    starting_population = [Lanternfish(int(timer))
                           for timer in raw_input[0].split(",")]

    print(
        f'Part 1 answer: {get_lanternfish_count(starting_population=starting_population, days=80)}')
    # print(
    #     f'Part 2 answer: {get_lanternfish_count(starting_population=starting_population, days=256)}')
