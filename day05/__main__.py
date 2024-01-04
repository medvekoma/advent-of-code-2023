import dataclasses
from typing import Optional, Iterator

from utils.enumerations import split_list_by
from utils.loader import Loader


@dataclasses.dataclass
class Mapping:
    target_start: int
    source_start: int
    length: int

    def convert(self, source: int) -> Optional[int]:
        if self.source_start <= source < self.source_start + self.length:
            offset = source - self.source_start
            return self.target_start + offset
        else:
            return None

    @staticmethod
    def convert_from_block(block: list['Mapping'], source: int) -> int:
        for mapping in block:
            target = mapping.convert(source)
            if target:
                return target
        return source


def get_seeds(block: list[str]) -> list[int]:
    line = next(iter(block))
    values = line.split(' ')[1:]
    return list(map(int, values))


def get_mappings(block: list[str]) -> Iterator[Mapping]:
    for item in block[1:]:
        values = item.split(' ')
        numbers = list(map(int, values))
        yield Mapping(*numbers)


def part1() -> int:
    locations: list[int] = list()
    for seed in seeds:
        transformed = seed
        for mappings in mappings_list:
            transformed = Mapping.convert_from_block(mappings, transformed)
        locations.append(transformed)
    return min(locations)


if __name__ == "__main__":
    lines = Loader.load("input.txt")
    blocks = split_list_by(lines, '')

    seeds = get_seeds(next(blocks))
    mappings_list = [
        list(get_mappings(block))
        for block in blocks
    ]
    print(f"part 1: {part1()}")


