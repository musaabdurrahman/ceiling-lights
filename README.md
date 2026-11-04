# 💡 Ceiling Light Planner

A Streamlit app that places lights in a rectangular block ceiling so that every light is evenly spaced and both walls are the same distance from the nearest light. It solves the problem with number theory rather than brute force, so rooms of any size are solved instantly.

## The mathematics

For one dimension of $D$ blocks, with $n$ lights, $g$ empty blocks between lights and $w$ empty blocks at each wall:

```math
D = 2w + n + (n-1)g
```

A configuration is valid when $w$ is a non-negative whole number, which gives:

- **Parity:** $D + g - n(g+1)$ must be even. If $g$ is odd, $D$ must be odd (and then every $n$ works); if $g$ is even, $n \equiv D \pmod 2$.
- **Bound:** $1 \le n \le \left\lfloor \frac{D+g}{g+1} \right\rfloor$.

The valid light counts therefore form an arithmetic sequence, returned as a Python `range` in O(1) time and memory. Light positions are another arithmetic sequence, $p_k = w + 1 + k(g+1)$. Width and length are solved independently, and the ceiling's lights are their Cartesian product.

**Closest configurations.** When no exact solution exists, the app offers the two smallest possible changes: the nearest gap $g'$ (minimising $|g' - g|$) that keeps perfect symmetry, or the same gap with one wall exactly one block wider. Both are computed directly.

Full derivations, including a geometric symmetry proof of the parity conditions, are in [MATH.md](MATH.md).

## Running it

```bash
git clone https://github.com/musaabdurrahman/ceiling-lights.git
cd ceiling-lights
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Run the tests with `python -m pytest`. They check the solver against hand-derived cases, a brute-force search of the definition, and symmetry properties.

## Project structure

| File | Layer |
|---|---|
| `MATH.md` | Mathematical model and derivations |
| `solver.py` | Algorithm and Python implementation (no UI code) |
| `test_solver.py` | Tests |
| `app.py` | Streamlit interface and grid drawing |