import dataclasses


@dataclasses.dataclass
class Range:
    start: int
    stop: int

    @staticmethod
    def from_start_count(start: int, count: int) -> "Range":
        return Range(start, start + count)

    def intersect(self, other: "Range") -> "Range":
        return Range(max(self.start, other.start), min(self.stop, other.stop))

    def contains(self, value: int) -> bool:
        return value in range(self.start, self.stop)

    def shift(self, offset: int) -> "Range":
        return Range(self.start + offset, self.stop + offset)

    def subtract(self, other: "Range") -> list["Range"]:
        result = [
            Range(self.start, min(self.stop, other.start)),
            Range(max(other.stop, self.start), self.stop),
        ]
        return [item for item in result if item.stop > item.start]

    def subtract_all(self, ranges: list["Range"]) -> list["Range"]:
        remaining_ranges = [self]
        for dropped_range in ranges:
            value: list["Range"] = list()
            for remaining_range in remaining_ranges:
                value += remaining_range.subtract(dropped_range)
            remaining_ranges = value
        return remaining_ranges
