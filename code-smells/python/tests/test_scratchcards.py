from pathlib import Path
from typing import List

import pytest

from src.scratchcards import (
    solve_part_one,
    calculate_row_points,
    calculate_row_matches,
    parse_numbers,
    solve_part_two,
    update_instances,
)


@pytest.fixture
def lines_stub() -> List[str]:
    source_path = Path(__file__).resolve().parent.parent.parent  / 'Scratchcards.md'
    with source_path.open("r") as file:
        return [line.strip() for line in file.readlines()[43:49]]


def test_calculate_victory_points(lines_stub):
    actual = solve_part_one(lines_stub)
    expected = 13
    assert actual == expected


def test_calculate_instances_grand_total(dict_stub):
    actual = solve_part_two(dict_stub)
    expected = 30
    assert actual == expected


@pytest.fixture
def dict_stub():
    return {
        1: 1,
        2: 2,
        3: 4,
        4: 8,
        5: 14,
        6: 1,
    }


@pytest.mark.parametrize(
    'matches, expected_points',
    [
        (4, 8),
        (2, 2),
        (1, 1),
        (0, 0),
    ],
)
def test_calculate_row_points(matches, expected_points):
    actual = calculate_row_points(matches)
    assert actual == expected_points


def test_calculate_row_matches(lines_stub):
    expected_matches = [4, 2, 2, 1, 0, 0]
    actual = [
        calculate_row_matches(
            parse_numbers(card_string), parse_numbers(winning_string)
        )
        for line in lines_stub
        for _, content in [line.split(": ")]
        for card_string, winning_string in [content.split("|")]
    ]
    assert actual == expected_matches


def test_update_instances(dict_stub, lines_stub):
    initial_dict = {index: 1 for index in range(1, 7)}
    actual = update_instances(initial_dict, lines_stub)
    assert actual == dict_stub
