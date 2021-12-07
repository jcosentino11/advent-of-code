
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import List
from util import get_input
from itertools import zip_longest


@dataclass(frozen=True)
class Point:
    """
    Representation of a coordinate pair
    """
    x: int
    y: int


@dataclass(frozen=True)
class Line:
    """
    Representation of a line on a graph
    """
    start: Point
    end: Point

    @staticmethod
    def from_input(input: str) -> Line:
        """
        Create a Line based on an input string.

           from_input('427,523 -> 427,790') == Line(x1=427, y1=523, x2=427, y2=790)
        """
        coords = [[int(n) for n in coords.split(',')] for coords in input.split(' -> ')]
        pairs = [Point(*coord) for coord in coords]
        return Line(*pairs)

    def is_horizontal(self) -> bool:
        """
        True if the line is horizontal
        """
        return self.start.y == self.end.y

    def is_vertical(self) -> bool:
        """
        True if the line is vertical
        """
        return self.start.x == self.end.x

    def is_diagonal(self) -> bool:
        """
        True if the line is diagonal
        """
        return not self.is_horizontal() and not self.is_vertical()

    def points(self) -> List[Point]:
        """
        Get all points on the line, inclusive of start and end points.
        This assumes that lines can only be horizontal or vertical.

          (1,1) (1,3)  -->  [Point(x=1,y=1), Point(x=1,y=2), Point(x=1,y=3)]
        """
        x_direction = 1 if self.end.x > self.start.x else -1
        y_direction = 1 if self.end.y > self.start.y else -1

        x_range = range(self.start.x, self.end.x + x_direction, x_direction)
        y_range = range(self.start.y, self.end.y + y_direction, y_direction)

        if self.is_horizontal():
            y_range = list(y_range) * len(x_range)
        elif self.is_vertical():
            x_range = list(x_range) * len(y_range)
        
        return [Point(x=x, y=y) for [x, y] in zip(x_range, y_range)]


def hydrothermal_venture(lines: List[Line], consider_diagonals=False, overlap_threshold: int = 2) -> int:    
    if not consider_diagonals:
        lines = [line for line in lines if not line.is_diagonal()]
    # flattened list of all points in all lines.
    # enjoy this very unreadable list comprehension ;)
    points = [point for points in [line.points() for line in lines] for point in points]
    # create mapping from point to their frequency
    point_frequency = defaultdict(int)
    for point in points:
        point_frequency[point] += 1
    # count how many overlaps occur 
    return sum([1 for frequency in point_frequency.values() if frequency >= overlap_threshold])


if __name__ == '__main__':
    raw_input = get_input(year=2021, day=5)
    lines = [Line.from_input(input) for input in raw_input]

    print(f'Part 1 answer: {hydrothermal_venture(lines, consider_diagonals=False)}')
    print(f'Part 2 answer: {hydrothermal_venture(lines, consider_diagonals=True)}')
