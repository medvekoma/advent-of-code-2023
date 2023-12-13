import math
from dataclasses import dataclass

from utils.loader import Loader


@dataclass
class Game:
    number: int
    hands: list[dict[str, int]]

    def __init__(self, text: str):
        game, all_hands_text = text.split(': ')
        self.number = int(game.replace("Game ", ""))
        self.hands = []
        for hand_text in all_hands_text.split("; "):
            hand: dict[str, int] = dict()
            for num_color in hand_text.split(", "):
                num, color = num_color.split(" ")
                hand[color] = int(num)
            self.hands.append(hand)


def is_valid_hand(hand: dict[str, int]) -> bool:
    for color, num in hand.items():
        if control_map[color] < num:
            return False
    return True


def is_valid_game(game: Game) -> bool:
    return all(map(is_valid_hand, game.hands))


def part1():
    valid_games = filter(is_valid_game, games)
    valid_game_numbers = [game.number for game in valid_games]
    print(f"part1: {sum(valid_game_numbers)}")


def get_max_hand(game: Game) -> dict[str, int]:
    max_hand: dict[str, int] = dict()
    for hand in game.hands:
        for color, num in hand.items():
            max_hand[color] = max(max_hand.get(color, 0), num)
    return max_hand


def part2():
    max_hands = [get_max_hand(game) for game in games]
    powers = [math.prod(max_hand.values()) for max_hand in max_hands]
    print(f"part2: {sum(powers)}")


if __name__ == "__main__":
    lines = Loader.load("input.txt")
    games = [Game(line) for line in lines]
    control_map = {
        "red": 12,
        "green": 13,
        "blue": 14
    }
    part1()
    part2()
