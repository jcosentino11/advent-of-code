
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from typing import List
from util import get_input


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

    def points(self) -> List[Point]:
        """
        Get all points on the line, inclusive of start and end points.
        This assumes that lines can only be horizontal or vertical.

          (1,1) (1,3)  -->  [Point(x=1,y=1), Point(x=1,y=2), Point(x=1,y=3)]
        """
        if self.is_horizontal():
            direction = 1 if self.end.x > self.start.x else -1
            return [Point(x=x, y=self.start.y) for x in range(self.start.x, self.end.x + direction, direction)]
        elif self.is_vertical():
            direction = 1 if self.end.y > self.start.y else -1
            return [Point(x=self.start.x, y=y) for y in range(self.start.y, self.end.y + direction, direction)]
        else:
            return []


def hydrothermal_venture(lines: List[Line], overlap_threshold: int = 2) -> int:    
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

    print(f'Part 1 answer: {hydrothermal_venture(lines)}')
    print(f'Part 2 answer: {hydrothermal_venture(lines)}')
