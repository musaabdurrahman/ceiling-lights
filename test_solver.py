import pytest

from solver import find_configurations


def test_31_gap_5_matches_hand_derivation():
    assert find_configurations(31, 5) == [
        (1, 15), (2, 12), (3, 9), (4, 6), (5, 3), (6, 0)
    ]


def test_38_gap_5_has_no_solution():
    # g is odd, so D must be odd; 38 is even.
    assert find_configurations(38, 5) == []


def test_negative_gap_is_rejected():
    with pytest.raises(ValueError):
        find_configurations(10, -1)

def test_38_gap_4_matches_hand_derivation():
    assert find_configurations(38, 4) == [
        (2,16), (4,11), (6,6), (8,1)
    ]

def test_2_gap_2_matches_hand_derivation():
    assert find_configurations(2, 2) == []

def test_dimension_less_than_1_is_rejected():
    with pytest.raises(ValueError):
        find_configurations(0, 1)

def test_gap_zero_matches_hand_derivation():
    assert find_configurations(10, 0) == [
        (2, 4) , (4, 3), (6, 2), (8, 1), (10, 0)
    ]

