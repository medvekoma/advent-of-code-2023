import dataclasses
import re

from utils.loader import Loader


@dataclasses.dataclass
class Card:
    number: int
    win_numbers: set[int]
    own_numbers: set[int]

    def __init__(self, text: str):
        card, numbers = text.split(": ")
        self.number = int(card.replace("Card ", ""))
        win, own = numbers.split(" | ")
        self.win_numbers = {int(num) for num in re.findall(r"\d+", win)}
        self.own_numbers = {int(num) for num in re.findall(r"\d+", own)}


def card_points1(card: Card) -> int:
    matching_numbers = card.win_numbers.intersection(card.own_numbers)
    matches = len(matching_numbers)
    if matches == 0:
        return 0
    return 2 ** (matches - 1)


def part1():
    points = [card_points1(card) for card in cards]
    print(f"part1: {sum(points)}")


def card_points2(card: Card) -> int:
    matching_numbers = card.win_numbers.intersection(card.own_numbers)
    return len(matching_numbers)


def part2():
    copied_cards = cards
    card_points = {
        card.number: card_points2(card)
        for card in cards
    }
    for card in copied_cards:
        points = card_points[card.number]
        start_index = card.number
        end_index = start_index + points
        new_cards = copied_cards[start_index:end_index]
        # print(start_index, end_index, [c.number for c in new_cards])
        copied_cards += new_cards
    card_count = len(copied_cards)
    print(f"part2: {card_count}")


if __name__ == "__main__":
    lines = Loader.load("input.txt")
    cards = [Card(line) for line in lines]
    part1()
    part2()
