import math
import operator
import re
import string

from utils.loader import Loader
from itertools import groupby


def _has_bounding_symbol(row: int, span: (int, int)) -> bool:
    r1 = max(0, row - 1)
    r2 = min(len(lines) - 1, row + 1)
    c1 = max(0, span[0] - 1)
    c2 = min(len(lines[0]) - 1, span[1])
    chars = [
        lines[r][c]
        for r in range(r1, r2 + 1)
        for c in range(c1, c2 + 1)
    ]
    bounding_string = "".join(chars)
    # print(f"  {bounding_string}")
    bounding_symbols = bounding_string.translate(str.maketrans("", "", string.digits + "."))
    return len(bounding_symbols) > 0


def part1():
    numbers = []
    for num, row, span in numbers_with_positions:
        # print(row, num, span)
        if _has_bounding_symbol(row, span):
            numbers.append(num)
    print(f"Part1: {sum(numbers)}")


def _get_gear_positions(row: int, span: (int, int)) -> list[(int, int)]:
    r1 = max(0, row - 1)
    r2 = min(len(lines) - 1, row + 1)
    c1 = max(0, span[0] - 1)
    c2 = min(len(lines[0]) - 1, span[1])
    return [
        (r, c)
        for r in range(r1, r2 + 1)
        for c in range(c1, c2 + 1)
        if lines[r][c] == "*"
    ]


def part2():
    gear_positions = [
        (gear_pos, num)
        for num, row, span in numbers_with_positions
        for gear_pos in _get_gear_positions(row, span)
    ]
    # print(gear_positions)
    gear_dict: dict[(int, int), list[int]] = dict()
    for gear_pos, num in gear_positions:
        if gear_pos in gear_dict:
            gear_dict[gear_pos].append(num)
        else:
            gear_dict[gear_pos] = [num]
    # print(gear_dict)
    powers = [
        math.prod(v)
        for k, v in gear_dict.items()
        if len(v) > 1
    ]
    print(f"Part2: {sum(powers)}")


if __name__ == "__main__":
    lines = Loader.load("input.txt")
    numbers_with_positions = [
        (int(match.group()), row, match.span())
        for row, line in enumerate(lines)
        for match in re.finditer(r"\d+", line)
    ]
    part1()
    part2()
