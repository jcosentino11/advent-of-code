
from dataclasses import dataclass
from typing import Dict, List
from util import get_input


@dataclass
class DiagnosticResult:
    power_consumption: int
    life_support_rating: int


def binary_diagnostic(report: List[int], num_binary_digits: int = 12) -> DiagnosticResult:

    def bit_value(number: int, index: int) -> int:
        """
        bit_value returns the bit at the given index.

        indexing is from left to right, to be consistent
        with the problem description.

            bit_value(0b1100, 0) == 1
            bit_value(0b1100, 1) == 1
            bit_value(0b1100, 2) == 0
            bit_value(0b1100, 3) == 0
        """
        offset = num_binary_digits - 1 - index
        mask = 0b1 << offset
        return (number & mask) >> offset

    def flip_bit(number: int, index: int) -> int:
        """
        flip_bit flips the bit at the given index.

        indexing is from left to right, to be consistent
        with the problem description.

            flip_bit(0b1100, 0) == 0100
            flip_bit(0b1100, 1) == 1000
            flip_bit(0b1100, 2) == 1110
            flip_bit(0b1100, 3) == 1101
        """
        offset = num_binary_digits - 1 - index
        return number ^ (0b1 << offset)

    def bit_frequencies(readings: List[int], index: int) -> Dict[int, int]:
        """
        bit_frequencies returns a mapping from a binary value to its
        number of occurances in readings, at the provided binary digit index

        indexing is from left to right, to be consistent
        with the problem description.

            bit_frequencies([0b10, 0b10, 0b11, 0b11], 0) == {0: 0, 1: 4}
            bit_frequencies([0b10, 0b10, 0b11, 0b11], 1) == {0: 2, 1: 2}
        """
        freq_one = sum([bit_value(number, index) for number in readings])
        return {
            0: len(readings) - freq_one,
            1: freq_one
        }

    def most_common_bit(frequencies: Dict[int, int], tiebreaker: int = 1) -> int:
        """
        most_common_bit returns the bit that occurs the most, given a frequency map.
        if there's a tie, return the tiebreaker value

            most_common_bit({0: 0, 1: 4}) == 1
            most_common_bit({0: 2, 1: 2}) == 1
            most_common_bit({0: 4, 1: 1}) == 0
        """
        if (frequencies[0] == frequencies[1]):
            return tiebreaker
        return max(frequencies, key=frequencies.get)

    def least_common_bit(frequencies: Dict[int, int], tiebreaker: int = 0) -> int:
        """
        least_common_bit returns the bit that occurs the least, given a frequency map.
        if there's a tie, return the tiebreaker value

            least_common_bit({0: 0, 1: 4}) == 0
            least_common_bit({0: 2, 1: 2}) == 0
            least_common_bit({0: 4, 1: 1}) == 1
        """
        if (frequencies[0] == frequencies[1]):
            return tiebreaker
        return min(frequencies, key=frequencies.get)

    # start with gamma and epsilon as all 1s.
    # throughout the algorithm, we flip some of
    # the 1s to 0s as necessary.
    gamma_rate = 2 ** num_binary_digits - 1
    epsilon_rate = 2 ** num_binary_digits - 1

    # for oxygen and c02, we narrow the list of measurements
    # every iteration, so each needs their own copy
    oxygen_report = report.copy()
    c02_report = report.copy()

    for index in range(num_binary_digits):
        # update gamma and epsilon rates
        report_bit_frequencies = bit_frequencies(report, index)
        if most_common_bit(report_bit_frequencies) == 0:
            # 0 is the most common bit
            # gamma_rate reflects most common bit,
            # so flip the pre-initialized 1 to a 0.
            # epsilon_rate remains unchanged, with a 1 at current index
            gamma_rate = flip_bit(gamma_rate, index)
        else:
            # 1 is the most common bit
            # epsilon_rate reflects the least common bit
            # so flip the pre-initialized 1 to a 0.
            # gamma_rate remains unchanged, with a 1 at current index
            epsilon_rate = flip_bit(epsilon_rate, index)

        # filter oxygen list by most common bit
        if len(oxygen_report) > 1:
            oxygen_bit_frequencies = bit_frequencies(oxygen_report, index)
            oxygen_report = [n for n in oxygen_report if
                             bit_value(n, index) == most_common_bit(oxygen_bit_frequencies)]

        # filter c02 list by least common bit
        if len(c02_report) > 1:
            c02_bit_frequencies = bit_frequencies(c02_report, index)
            c02_report = [n for n in c02_report if
                          bit_value(n, index) == least_common_bit(c02_bit_frequencies)]

    oxygen_generator_rating = oxygen_report[0]
    co2_scrubber_rating = c02_report[0]

    power_consumption = gamma_rate * epsilon_rate
    life_support_rating = oxygen_generator_rating * co2_scrubber_rating

    return DiagnosticResult(power_consumption=power_consumption,
                            life_support_rating=life_support_rating)


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=3)
    report = list(map(lambda x: int(x, 2), raw_input))

    result = binary_diagnostic(report, num_binary_digits=len(raw_input[0]))

    print(f'Part 1 answer: {result.power_consumption}')
    print(f'Part 2 answer: {result.life_support_rating}')
