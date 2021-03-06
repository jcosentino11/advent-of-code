from __future__ import annotations
from abc import abstractmethod
from typing import Dict, List, Optional
from util import get_input
from dataclasses import dataclass


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


@dataclass
class SimulationConfiguration:
    "Starting population of lanternfish"
    starting_population: List[Lanternfish]
    "Whether verbose logging is enabled"
    verbose: bool = False


class LanternfishSimulation:

    def __init__(self, conf: SimulationConfiguration) -> None:
        self.conf = conf
        "How long the simulation has run so far"
        self.days_elapsed: int = 0

    @abstractmethod
    def population_size(self) -> int:
        """
        Returns the size of the current population
        """
        pass

    def next_day(self) -> None:
        """
        Run the next day of simulation for the entire population of fish
        """
        self._next_day()
        self.days_elapsed += 1

    @abstractmethod
    def _next_day(self) -> None:
        pass


class NaiveSimulation(LanternfishSimulation):
    """
    Naive approach.

    Represent all lanternfish timers as list. Each day,
    iterate through the whole population and append newly spawned
    fish to the list.  This approach isn't great because list
    grows very large as the simulation progresses.
    """

    def __init__(self, conf: SimulationConfiguration) -> None:
        super().__init__(conf)
        "Current population of lanternfish"
        self._population: List[Lanternfish] = conf.starting_population

    def population_size(self) -> int:
        """
        Returns the size of the current population
        """
        return len(self._population)

    def _next_day(self):
        new_fish = []

        for fish in self._population:
            spawned_fish = fish.next_day()
            if spawned_fish:
                new_fish.append(spawned_fish)

        self._population.extend(new_fish)

        if self.conf.verbose:
            print(
                f'After {self.days_elapsed + 1} day(s): {",".join([str(fish._timer) for fish in self._population])}')


class OptimizedSimulation(LanternfishSimulation):
    """
    Optimized approach.

    Represent lanternfish as list of timer value frequencies.
    This approach is bounded by the number of possible timer values, rather
    than the size of the lanternfish population, making it much more performant
    over the naive approach.
    """

    MAX_NUM_TIMER_VALUES = 9

    def __init__(self, conf: SimulationConfiguration) -> None:
        super().__init__(conf)
        "Current population of lanternfish"
        self._population: List[int] = [0] * \
            OptimizedSimulation.MAX_NUM_TIMER_VALUES
        for fish in conf.starting_population:
            self._population[fish._timer] += 1

    def population_size(self) -> int:
        """
        Returns the size of the current population
        """
        return sum(self._population)

    def _next_day(self):
        num_expired_timers = self._population[0]
        # decrement timer values 
        self._population.pop(0)
        # expired timers reset at value 6
        self._population[6] += num_expired_timers
        # new fish are spwaned with timer value 8
        self._population.append(num_expired_timers)


def get_lanternfish_counts(simulation: LanternfishSimulation, days: List[int]) -> Dict[int, int]:
    days = sorted(days)
    counts = {}
    for day in range(1, days[-1] + 1):
        simulation.next_day()
        if day in days:
            counts[day] = simulation.population_size()
    return counts


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=6)
    starting_population = [Lanternfish(int(timer))
                           for timer in raw_input[0].split(",")]

    conf = SimulationConfiguration(
        starting_population=starting_population,
        # verbose=True
    )

    # simulation = NaiveSimulation(conf)
    simulation = OptimizedSimulation(conf)

    population_at_day = get_lanternfish_counts(simulation, days=[80, 256])

    print(
        f'Part 1 answer: {population_at_day[80]}')
    print(
        f'Part 2 answer: {population_at_day[256]}')
