import dataclasses
from typing import Optional, Iterator

from utils.enumerations import split_list_by
from utils.loader import Loader
from utils.range_helper import Range


@dataclasses.dataclass
class Mapping:
    source_range: Range
    target_offset: int

    @staticmethod
    def from_input(target_start: int, source_start: int, count: int) -> "Mapping":
        return Mapping(
            Range.from_start_count(source_start, count),
            target_start - source_start,
        )

    def map(self, source: int) -> Optional[int]:
        if self.source_range.contains(source):
            return source + self.target_offset
        else:
            return None

    @staticmethod
    def map_with_block(source: int, block: list["Mapping"]) -> int:
        for mapping in block:
            target = mapping.map(source)
            if target:
                return target
        return source


def get_seeds(block: list[str]) -> list[int]:
    line = next(iter(block))
    values = line.split(" ")[1:]
    return list(map(int, values))


def get_mappings(block: list[str]) -> Iterator[Mapping]:
    for item in block[1:]:
        values = item.split(" ")
        numbers = list(map(int, values))
        yield Mapping.from_input(*numbers)


def part1() -> int:
    locations: list[int] = list()
    for seed in seeds:
        transformed = seed
        for mappings in mappings_list:
            transformed = Mapping.map_with_block(transformed, mappings)
        locations.append(transformed)
    return min(locations)


def part2() -> int:
    def get_seed_ranges() -> list[Range]:
        return [
            Range.from_start_count(seeds[i], count=seeds[i + 1])
            for i in range(0, len(seeds), 2)
        ]

    def map_range(source: Range, mappings: list[Mapping]) -> list[Range]:
        active_mappings = [
            Mapping(source.intersect(mapping.source_range), mapping.target_offset)
            for mapping in mappings
        ]
        active_mappings = [
            mapping
            for mapping in active_mappings
            if mapping.source_range.stop > mapping.source_range.start
        ]
        result = [
            mapping.source_range.shift(mapping.target_offset)
            for mapping in active_mappings
        ]
        mapped_ranges = [mapping.source_range for mapping in active_mappings]
        result += source.subtract_all(mapped_ranges)
        return result

    def map_ranges(source_ranges: list[Range], mappings: list[Mapping]) -> list[Range]:
        result: list[Range] = list()
        for source in source_ranges:
            result += map_range(source, mappings)
        return result

    ranges = get_seed_ranges()
    for _mappings in mappings_list:
        ranges = map_ranges(ranges, _mappings)
    starts = [_range.start for _range in ranges]
    return min(starts)


if __name__ == "__main__":
    lines = Loader.load("input.txt")
    blocks = split_list_by(lines, "")

    seeds = get_seeds(next(blocks))
    mappings_list = [list(get_mappings(block)) for block in blocks]
    print(f"part 1: {part1()}")
    print(f"part 2: {part2()}")
