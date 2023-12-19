from copy import deepcopy
import re
from pathlib import Path
from typing import Set, Dict, List


def parse_numbers(line_with_numbers: str) -> Set[int]:
    pattern = re.compile(r"\d+")
    return set(pattern.findall(line_with_numbers))


def calculate_row_matches(
        card_numbers: Set[int],
        winning_numbers: Set[int],
) -> int:
    return len([num for num in card_numbers if num in winning_numbers])


def calculate_row_points(card_matches: int) -> int:
    return 0 if card_matches == 0 else 2 ** (card_matches - 1)


def solve_part_one(all_lines):
    number_of_matches = [
        calculate_row_matches(
            parse_numbers(card_string),
            parse_numbers(winning_string),
        )
        for line in all_lines
        for _, content in [line.split(":")]
        for card_string, winning_string in [content.split("|")]
    ]
    return sum([calculate_row_points(matches) for matches in number_of_matches])


def solve_part_two(all_instances):
    return sum(all_instances.values())


def update_instances(
        cards_instances: Dict[int, int], remaining_lines: List[str],
) -> Dict[int, int]:
    dict_copy = deepcopy(cards_instances)
    if not remaining_lines:
        return dict_copy

    line, *rest = remaining_lines
    card_id, content = line.split(":")
    card_string, winning_string = content.split("|")

    base_key = int(*list(parse_numbers(card_id)))
    instances = dict_copy[base_key]
    card_matches = calculate_row_matches(
        parse_numbers(card_string),
        parse_numbers(winning_string),
    )

    for accumulator in range(1, card_matches + 1):
        key = base_key + accumulator
        dict_copy[key] += instances
    return update_instances(dict_copy, rest)


def main():

    file_path = Path(__file__).parent / "input.txt"
    with open(file_path) as file:
        lines = file.readlines()
    first_answer = solve_part_one(lines)
    print("The answer is", first_answer)
    initial_instances = {index: 1 for index in range(1, len(lines) + 1)}
    all_instances = update_instances(initial_instances, lines)
    second_answer = solve_part_two(all_instances)
    print("The final answer is", second_answer)


if __name__ == "__main__":
    main()
