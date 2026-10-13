# def find_configurations(dimension: int, gap: int) -> list[tuple[int, int]]:
#     """Return every valid (lights, wall) configuration for one dimension.

#     A configuration is valid when
#         dimension = 2 * wall + lights + (lights - 1) * gap
#     with lights >= 1 and wall >= 0, all whole numbers.
#     Results are ordered by number of lights, smallest first.
#     """
#     if dimension < 1:
#         raise ValueError("dimension must be at least 1")
#     if gap < 0:
#         raise ValueError("gap must be non-negative")

#     max_lights = (dimension + gap) // (gap + 1)
#     configurations = []


#     #Four cases for (D,g) - if D is even and g is odd, there are no valid configurations.
#     #If D is even and g is even, the first n will be two (two lights beside the middle) and the step between valid n's will be two
#     #If D is odd and g is even, the first n will be one (one light in the middle) and the step between valid n's will be two
#     #If D is odd and g is odd, the first n will be one (one light in the middle) and the step between valid n's will be one to account for the alternating cases where either there is a light in the middle or there is the middle of a gap in the middle


#     if dimension % 2 == 0 and gap % 2 == 1:
#         # If D is even and g is odd, there are no valid configurations.
#         return []

#     if dimension % 2 == 0:
#         first = 2
#     else:
#         first = 1

#     if gap % 2 == 0:
#         step = 2
#     else:
#         step = 1
    

#     for lights in range(first, max_lights + 1, step):
#         numerator = dimension + gap - lights * (gap + 1) #computes D+g-n(g+1)
#         assert numerator % 2 == 0
#         wall = numerator // 2 #w=(D+g-n(G+1))/2
#         assert wall >= 0 #for loop ensures the number of lights never exceeds (D+g)/(g+1), so wall is always non-negative
#         configurations.append((lights, wall))

#     return configurations

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



if __name__ == "__main__":
    print(find_configurations(31, 5))
    print(find_configurations(38, 5))
    print(find_configurations(38, 4))
    print(find_configurations(2, 2))