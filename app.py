"""Streamlit interface for the ceiling light pattern generator.

Run with:  streamlit run app.py
All the mathematics lives in solver.py; this file only handles input and display.
"""

import numpy as np
import streamlit as st

from solver import (
    CeilingLayout,
    alternative_gaps,
    light_positions,
    nearest_light_count,
    valid_light_counts,
    wall_spacing,
)

MAX_OPTIONS = 200       # list configurations in a dropdown up to this many
MAX_DRAWN_BLOCKS = 200  # largest number of blocks drawn along each side

LIGHT = (255, 200, 40)
MARGIN = (205, 205, 210)
CEILING = (240, 240, 242)
GRID = (150, 150, 155)


def row_diagram(left_wall: int, lights: int, gap: int, right_wall: int) -> str:
    """Text picture of one row, e.g. '3 | 💡 | 5 | 💡 | 3'."""
    if lights <= 9:
        middle = f" | {gap} | ".join(["💡"] * lights)
    else:
        three = f" | {gap} | ".join(["💡"] * 3)
        middle = f"{three} | {gap} | … {lights - 6:,} more lights … | {gap} | {three}"
    return f"{left_wall} | {middle} | {right_wall}"


def choose_dimension(label: str, dimension: int, gap: int, key: str) -> range:
    """Show the options for one dimension and return the chosen light positions."""
    st.subheader(f"{label}: {dimension:,} blocks")
    solve_size, solve_gap, uneven = dimension, gap, False
    counts = valid_light_counts(dimension, gap)

    if counts:
        st.success(f"{len(counts):,} exact configurations with a {gap}-block gap.")
    else:
        st.warning(f"No exact symmetric configuration exists with a {gap}-block gap.")
        options = {
            f"Use a {g}-block gap instead": (dimension, g, False)
            for g in alternative_gaps(dimension, gap)
        }
        # Solving D - 1 and leaving the spare block at the far wall gives
        # walls of w and w + 1: the smallest possible asymmetry.
        options[f"Keep the {gap}-block gap; one wall is a block wider"] = (
            dimension - 1, gap, True,
        )
        choice = st.radio("Closest alternatives", list(options),
                          key=f"{key}_alt_{dimension}_{gap}")
        solve_size, solve_gap, uneven = options[choice]
        counts = valid_light_counts(solve_size, solve_gap)

    # Default: walls about half a gap wide, as if the pattern continued.
    default = nearest_light_count(solve_size, solve_gap, solve_gap // 2)
    widget_key = f"{key}_{solve_size}_{solve_gap}"

    if len(counts) <= MAX_OPTIONS:
        options_list = list(counts)
        lights = st.selectbox(
            "Wall spacing",
            options_list,
            index=options_list.index(default),
            format_func=lambda n: (
                f"{wall_spacing(solve_size, solve_gap, n)} blocks from the wall"
                f" · {n} lights"
            ),
            key=widget_key,
        )
    else:
        preferred = st.number_input("Preferred wall spacing", min_value=0,
                                    value=solve_gap // 2, step=1, key=widget_key)
        lights = nearest_light_count(solve_size, solve_gap, int(preferred))
        st.caption(f"{len(counts):,} configurations exist; "
                   "the one nearest your preference is shown.")

    wall = wall_spacing(solve_size, solve_gap, lights)
    right_wall = wall + 1 if uneven else wall
    walls = f"{wall} and {right_wall}" if uneven else f"{wall}"
    st.markdown(f"**Wall spacing:** {walls} · **Lights:** {lights:,} · **Gap:** {solve_gap}")
    st.code(row_diagram(wall, lights, solve_gap, right_wall), language=None)

    positions = light_positions(solve_size, solve_gap, lights)
    shown = ", ".join(str(p) for p in positions[:20])
    more = ", …" if len(positions) > 20 else ""
    st.caption(f"Light positions: {shown}{more}")
    return positions


def ceiling_image(layout: CeilingLayout, width: int, length: int) -> np.ndarray:
    """Draw the ceiling (or its top-left corner, if huge) as an RGB image."""
    shown_w = min(width, MAX_DRAWN_BLOCKS)
    shown_l = min(length, MAX_DRAWN_BLOCKS)
    xs, ys = layout.x_positions, layout.y_positions

    # has_light is O(1), so drawing costs one check per visible block.
    lights = np.array([[layout.has_light(x, y) for x in range(1, shown_w + 1)]
                       for y in range(1, shown_l + 1)])
    x_margin = np.array([x < xs[0] or x > xs[-1] for x in range(1, shown_w + 1)])
    y_margin = np.array([y < ys[0] or y > ys[-1] for y in range(1, shown_l + 1)])
    margin = y_margin[:, None] | x_margin[None, :]

    image = np.empty((shown_l, shown_w, 3), dtype=np.uint8)
    image[:] = CEILING
    image[margin] = MARGIN
    image[lights] = LIGHT

    # Scale each block up to a square of pixels and draw grid lines.
    cell = max(3, min(24, 720 // max(shown_w, shown_l)))
    image = image.repeat(cell, axis=0).repeat(cell, axis=1)
    image[cell - 1::cell, :] = GRID
    image[:, cell - 1::cell] = GRID
    return image


st.set_page_config(page_title="Ceiling Light Planner", page_icon="💡")
st.title("💡 Ceiling Light Planner")
st.write(
    "Place lights in a rectangular ceiling so that the lights are evenly spaced "
    "and both walls are the same distance from the nearest light. "
    "Solutions are calculated directly from number theory, so huge rooms work instantly."
)

col1, col2 = st.columns(2)
width = int(col1.number_input("Width (blocks)", min_value=1, value=31, step=1))
length = int(col2.number_input("Length (blocks)", min_value=1, value=38, step=1))
gap = int(st.number_input("Gap between lights (blocks)", min_value=0, value=5, step=1))
if st.checkbox("Use a different gap along the length"):
    length_gap = int(st.number_input("Gap along the length (blocks)",
                                     min_value=0, value=gap, step=1))
else:
    length_gap = gap

st.divider()
left, right = st.columns(2)
with left:
    xs = choose_dimension("Width", width, gap, "width")
with right:
    ys = choose_dimension("Length", length, length_gap, "length")

layout = CeilingLayout(x_positions=xs, y_positions=ys)

st.divider()
st.subheader("Ceiling")
st.metric("Total lights", f"{layout.total_lights():,}")

caption = "Width runs left to right, length top to bottom. Yellow: lights. Darker grey: wall margins."
if width > MAX_DRAWN_BLOCKS or length > MAX_DRAWN_BLOCKS:
    caption += f" Large room: showing the top-left {MAX_DRAWN_BLOCKS} × {MAX_DRAWN_BLOCKS} blocks."
st.image(ceiling_image(layout, width, length), caption=caption)