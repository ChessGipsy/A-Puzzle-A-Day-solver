# A-Puzzle-A-Day-solver

# Geometric Calendar Puzzle Solver 🧩📅

**Find an exact tiling that leaves _only_ a chosen month & day uncovered.**

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python">
  <img src="https://img.shields.io/badge/License-MIT-green">
</div>

## What is this?

You know that wooden calendar puzzle with eight funky polyomino pieces?  
The goal is to cover a board of 43 squares so that **exactly two—one month cell
and one day cell—stay visible**, forming any date you choose (e.g. **6 July**).

This repo contains a **drop-in Python 3 solver** that:

* Accepts a date on the command line (`python geopuzzle_solver.py July 6`)
* Finds a valid tiling (if one exists) using Algorithm X (exact cover)
* Prints:
  * Machine-readable placement data
  * An ASCII drawing of the fitted board
  * Search statistics (tries + run-time)

No external dependencies, pure standard-library code.

---

## Quick start

```bash
# Clone and run (requires Python 3.9+)
git clone https://github.com/<your-user>/geometric-calendar-solver.git
cd geometric-calendar-solver

python geopuzzle_solver.py July 6      # month spelled out
python geopuzzle_solver.py 7 6         # or numeric month
