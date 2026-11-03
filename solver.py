"""Mathematical solver for symmetric, evenly spaced ceiling lights.

For one dimension D with gap g, a configuration of n lights and wall
spacing w is valid when D = 2w + n + (n - 1)g, with n >= 1 and w >= 0,
all whole numbers. See MATH.md for the derivation.
Blocks are numbered from 1.
"""

from dataclasses import dataclass

def valid_light_counts(dimension: int, gap: int) -> range:
    """Return every valid number of lights, as a range.

    Uses O(1) time and memory regardless of dimension: the range stores
    only its start, stop and step, and computes elements on demand.
    """
    if dimension < 1:
        raise ValueError("dimension must be at least 1")
    if gap < 0:
        raise ValueError("gap must be non-negative")

    if gap % 2 == 1 and dimension % 2 == 0:
        return range(0)  # an empty range

    max_lights = (dimension + gap) // (gap + 1)
    first = 1 if dimension % 2 == 1 else 2
    step = 1 if gap % 2 == 1 else 2
    return range(first, max_lights + 1, step)


def wall_spacing(dimension: int, gap: int, lights: int) -> int:
    """Return the wall spacing w for a valid number of lights."""
    numerator = dimension + gap - lights * (gap + 1)
    assert numerator >= 0 and numerator % 2 == 0
    return numerator // 2


def find_configurations(dimension: int, gap: int) -> list[tuple[int, int]]:
    """Return every valid (lights, wall) pair as a list.

    Convenient for small dimensions; the list grows with the number
    of solutions, so use valid_light_counts for very large rooms.
    """
    return [
        (lights, wall_spacing(dimension, gap, lights))
        for lights in valid_light_counts(dimension, gap)
    ]

def light_positions(dimension: int, gap: int, lights: int) -> range:
    """Return the block positions of the lights, numbered from 1.

    The k-th light (from k = 0) is at w + 1 + k(g + 1); the last is at D - w.
    """
    wall = wall_spacing(dimension, gap, lights)
    return range(wall + 1, dimension - wall + 1, gap + 1)



def nearest_light_count(dimension: int, gap: int, preferred_wall: int) -> int | None:
    """Return the valid number of lights whose wall spacing is closest to
    preferred_wall, or None if no configuration exists.

    O(1): solving w = preferred for n gives n(g + 1) = D + g - 2w, so we find
    where that n falls in the range of valid counts and compare the two
    neighbouring valid counts. Ties go to fewer lights.
    """
    counts = valid_light_counts(dimension, gap)
    if not counts:
        return None

    period = gap + 1
    target = dimension + gap - 2 * preferred_wall
    k = (target - counts.start * period) // (counts.step * period)
    last = len(counts) - 1
    candidates = {counts[min(max(i, 0), last)] for i in (k, k + 1)}
    return min(
        candidates,
        key=lambda n: (abs(wall_spacing(dimension, gap, n) - preferred_wall), n),
    )


def alternative_gaps(dimension: int, gap: int) -> list[int]:
    """Return the gaps nearest to `gap` that do have an exact configuration.

    Returns [] if `gap` already works. "Nearest" means smallest |g' - g|.

    Only an even dimension can lack a solution: an odd one always fits a
    single centred light. An even dimension needs an even gap of at most
    D - 2 (two lights either side of the centre line). So the answer is
    found directly, with no search.
    """
    if valid_light_counts(dimension, gap):
        return []

    largest_gap = dimension - 2
    if gap > largest_gap:
        return [largest_gap]
    return [gap - 1, gap + 1]  # gap is odd here, so both neighbours are even


@dataclass(frozen=True)
class CeilingLayout:
    """A rectangular ceiling's lights, described by their positions.

    A light sits at every (x, y) where x is in x_positions (along the width)
    and y is in y_positions (along the length). Blocks are numbered from 1.
    """

    x_positions: range
    y_positions: range

    def total_lights(self) -> int:
        return len(self.x_positions) * len(self.y_positions)

    def has_light(self, x: int, y: int) -> bool:
        return x in self.x_positions and y in self.y_positions


def ceiling_layout(
    width: int, width_gap: int, width_lights: int,
    length: int, length_gap: int, length_lights: int,
) -> CeilingLayout:
    """Build the layout for a width × length ceiling.

    Each direction is solved independently, with its own gap.
    """
    return CeilingLayout(
        x_positions=light_positions(width, width_gap, width_lights),
        y_positions=light_positions(length, length_gap, length_lights),
    )



if __name__ == "__main__":
    print(find_configurations(31, 5))
    print(find_configurations(38, 5))
    print(alternative_gaps(38, 5))
    print(ceiling_layout(31, 5, 5, 38, 4, 8).total_lights())