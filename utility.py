import math
from enum import Enum


class Color(Enum):
    RED = 100
    BLUE = 200
    GREEN = 300

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


class Tile:
    def __init__(self, num: int, color: Color):
        self.num = num
        self.color = color

    def __lt__(self, other):
        if self.num == other.num:
            return self.color < other.color
        return self.num < other.num

    def __eq__(self, other):
        return self.num == other.num and self.color == other.color

    def __repr__(self):
        return f"Tile<{self.num}, {self.color}>"

    def __str__(self):
        escape_sequence = ""
        if self.color == Color.RED:
            escape_sequence = "\033[31m"
        elif self.color == Color.BLUE:
            escape_sequence = "\033[34m"
        elif self.color == Color.GREEN:
            escape_sequence = "\033[32m"
        return escape_sequence + str(self.num) + "\033[39m"


class Hand:
    def __init__(self, tiles: list[Tile]):
        self.tiles = tiles[:5]
        self.sort()

    def sort(self):
        self.tiles.sort()

    def __repr__(self):
        return f"Hand<{' '.join(map(str, self.tiles))}>"


def calc_entropy(cases: list[int]) -> float:
    s = sum(cases)
    return sum(map(lambda num: math.log2(s / num) * num, cases)) / s


if __name__ == "__main__":
    pass
