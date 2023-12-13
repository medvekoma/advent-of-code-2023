import string
import re
from num2words import num2words
from utils.loader import Loader


def part1():
    result = 0
    for line in lines:
        stripped = line.strip(string.ascii_letters)
        s = stripped[0] + stripped[-1]
        num = int(s)
        result += num
    print(f"part1: {result}")


def part2():
    number_map = {
        num2words(i): str(i)
        for i in range(1, 10)
    }
    pattern = '|'.join(list(number_map.keys()) + list(number_map.values()))
    pattern = f"(?=({pattern}))"
    # print(pattern)
    result = 0
    for line in lines:
        # print(line)
        res = re.findall(pattern, line)
        res = [number_map.get(match, match) for match in res]
        s = res[0] + res[-1]
        # print(res, s)
        num = int(s)
        result += num
    print(f"part2: {result}")


if __name__ == "__main__":
    lines = Loader.load("input01.txt")
    part1()
    part2()
