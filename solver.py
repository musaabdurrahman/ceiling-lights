def find_configurations(dimension: int, gap: int) -> list[tuple[int, int]]:
    """Return every valid (lights, wall) configuration for one dimension.

    A configuration is valid when
        dimension = 2 * wall + lights + (lights - 1) * gap
    with lights >= 1 and wall >= 0, all whole numbers.
    Results are ordered by number of lights, smallest first.
    """
    if dimension < 1:
        raise ValueError("dimension must be at least 1")
    if gap < 0:
        raise ValueError("gap must be non-negative")

    max_lights = (dimension + gap) // (gap + 1)
    configurations = []

    for lights in range(1, max_lights + 1):
        numerator = dimension + gap - lights * (gap + 1) #computes D+g-n(g+1)
        if numerator % 2 == 0:
            wall = numerator // 2 #w=(D+g-n(G+1))/2
            assert wall >= 0 #for loop ensures the number of lights never exceeds (D+g)/(g+1), so wall is always non-negative
            configurations.append((lights, wall))

    return configurations


if __name__ == "__main__":
    print(find_configurations(31, 5))
    print(find_configurations(38, 5))
    print(find_configurations(38, 4))
    print(find_configurations(2, 2))