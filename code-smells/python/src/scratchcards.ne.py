from copy import deepcopy
import re
from pathlib import Path
from typing import Set, Dict, List


def main():

    def calculate_row_matches(
        card_numbers: Set[int],
        winning_numbers: Set[int],
    ) -> int:
        return len([num for num in card_numbers if num in winning_numbers])

    def calculate_row_points(card_matches: int) -> int:
        return 0 if card_matches == 0 else 2 ** (card_matches - 1)

    def calculate_victory_points(all_lines):
        games = []
        for line in all_lines:
            for head, content in [line.split(":")]:
                for card_string, winning_string in [content.split("|")]:
                    pattern = re.compile(r"\d+")
                    numbers = set(pattern.findall(card_string))
                    winning_row = set(pattern.findall(winning_string))
                    games.append((numbers, winning_row))
        number_of_matches = []
        for numbers_and_winning_row in games:
            good_numbers = calculate_row_matches(numbers_and_winning_row[0], numbers_and_winning_row[1])
            number_of_matches.append(good_numbers)
        total = 0
        for matching_numbers in number_of_matches:
            total += matching_numbers

    def update_instances(
        cards_instances: Dict[int, int], remaining_lines: List[str],
    ) -> Dict[int, int]:
        rest = remaining_lines
        while len(rest) >0:
            if not rest:
                return cards_instances

            line, *rest = remaining_lines
            card_id, content = line.split(":")
            card_string, winning_string = content.split("|")

            base_key = int(*list(parse_numbers(card_id)))
            instances = cards_instances[base_key]
            card_matches = calculate_row_matches(
                parse_numbers(card_string),
                parse_numbers(winning_string),
            )

            for a in range(1, card_matches + 1):
                key = base_key + a
                cards_instances[key] += instances

    file_path = Path(__file__).parent / "input.txt"
    with open(file_path) as file:
        lines = file.readlines()

    games = []
    for line in lines:
        for head, content in [line.split(":")]:
            for card_string, winning_string in [content.split("|")]:
                pattern = re.compile(r"\d+")
                numbers = set(pattern.findall(card_string))
                winning_row = set(pattern.findall(winning_string))
                games.append((numbers, winning_row))
    number_of_matches = []
    for numbers_and_winning_row in games:
        good_numbers = calculate_row_matches(numbers_and_winning_row[0], numbers_and_winning_row[1])
        number_of_matches.append(good_numbers)
    total = 0
    for matching_numbers in number_of_matches:
        total += matching_numbers
    first_answer = total
    print("The first answer is", first_answer)
    initial_instances = {}
    i = 0
    while i < len(lines):
        initial_instances[i] = i + 1
        i = i + 1
    all_instances = update_instances(initial_instances, lines)
    total = 0
    for key, value in all_instances.items():
        total = total + value
    second_answer = total
    print("The final answer is", second_answer)


if __name__ == "__main__":
    main()
