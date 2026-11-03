"""Streamlit interface for the ceiling light pattern generator.

Run with:  streamlit run app.py
All the mathematics lives in solver.py; this file only handles input and display.
"""

import streamlit as st

from solver import (
    light_positions,
    nearest_light_count,
    valid_light_counts,
    wall_spacing,
    alternative_gaps
)

MAX_OPTIONS = 200  # list configurations in a dropdown up to this many


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