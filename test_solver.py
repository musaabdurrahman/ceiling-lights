import pytest

from solver import find_configurations, valid_light_counts, wall_spacing, light_positions


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

def brute_force_configurations(dimension: int, gap: int) -> list[tuple[int, int]]:
    """Return every valid (lights, wall) configuration for one dimension.

    A configuration is valid when
        dimension = 2 * wall + lights + (lights - 1) * gap
    with lights >= 1 and wall >= 0, all whole numbers.
    Results are ordered by number of lights, smallest first.

    This is a brute-force implementation for testing purposes - it uses the raw definition of a valid configuration, rather than the derived formula used in find_configurations.
    Try every possible number of lights and wall gaps, and check if the configuration is valid. This is much slower than find_configurations, but it is guaranteed to be correct.
    """
    configurations = []
    for lights in range(1, dimension + 1):
        for wall in range(0, dimension + 1):
            if dimension == 2 * wall + lights + (lights - 1) * gap:
                configurations.append((lights, wall))

    return configurations

def test_find_configurations_matches_brute_force():
    for dimension in range(1, 60):
        for gap in range(0, 15):
            assert find_configurations(dimension, gap) == brute_force_configurations(dimension, gap), f"Mismatch for D={dimension}, g={gap}"


def test_huge_dimension_is_described_without_listing():
    dimension, gap = 10**12 + 1, 5
    lights = valid_light_counts(dimension, gap)

    assert len(lights) > 10**11  # far too many to list

    # Spot-check the first and last solutions against the definition.
    for n in (lights[0], lights[-1]):
        w = wall_spacing(dimension, gap, n)
        assert w >= 0
        assert dimension == 2 * w + n + (n - 1) * gap


def test_list_light_positions_31_5_5():
    assert list(light_positions(31, 5, 5)) == [4, 10, 16, 22, 28]

def test_light_positions_are_symmetric():
    for dimension in range(1, 60):
        for gap in range(0, 15):
            for lights in valid_light_counts(dimension, gap):
                positions = list(light_positions(dimension, gap, lights))

                assert len(positions) == lights, (
                    f"Wrong count for D={dimension}, g={gap}, n={lights}"
                )

                for left, right in zip(positions, reversed(positions)):
                    assert left + right == dimension + 1, (
                        f"Not symmetric for D={dimension}, g={gap}, n={lights}"
                    )