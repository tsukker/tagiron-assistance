import functools
import math
import unicodedata
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


def colorize(s: str):
    replacing_list = (
        ("<Color.RED>", "\033[31m"),
        ("</Color.RED>", "\033[39m"),
        ("<Color.BLUE>", "\033[34m"),
        ("</Color.BLUE>", "\033[39m"),
        ("<Color.GREEN>", "\033[32m"),
        ("</Color.GREEN>", "\033[39m"),
    )
    return functools.reduce(lambda s_tmp, item: s_tmp.replace(item[0], item[1]), replacing_list, s)


def strip_coloring_tag(s: str):
    replacing_list = (
        ("<Color.RED>", ""),
        ("</Color.RED>", ""),
        ("<Color.BLUE>", ""),
        ("</Color.BLUE>", ""),
        ("<Color.GREEN>", ""),
        ("</Color.GREEN>", ""),
    )
    return functools.reduce(lambda s_tmp, item: s_tmp.replace(item[0], item[1]), replacing_list, s)


def entire_east_asian_width(s: str):
    cnt = 0
    for c in strip_coloring_tag(s):
        if unicodedata.east_asian_width(c) in "FWA":
            cnt += 2
        else:
            cnt += 1
    return cnt


def ljust_east_asian(s: str, width: int, c: str = " "):
    assert c == " "
    num_added = max(0, width - entire_east_asian_width(s))
    return s + (c * num_added)


if __name__ == "__main__":
    pass
