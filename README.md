# A-Puzzle-A-Day Solver 🧩📅

_Find an exact tiling that leaves **only one month square and one day square** uncovered._

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python">
  <img src="https://img.shields.io/badge/License-MIT-green">
</div>

## What is this?

“A-Puzzle-A-Day” is a wooden calendar puzzle consisting of eight polyomino
pieces and an irregular 43-cell board.  
For any requested date (e.g. **6 July**) the goal is to place every piece so
_that_ the month cell **July** and the day cell **6** remain visible while all
other cells are covered.

This repo provides a **stand-alone Python 3 solver** that:

* accepts a date on the command line  
  `python apuzzle_solver.py July 6`
* searches for a valid tiling (Algorithm X / exact cover)
* prints
  * machine-readable placement data
  * an ASCII drawing of the finished board
  * statistics (number of tries, elapsed time)

No external dependencies — pure standard library.

---

## Quick start

```bash
git clone https://github.com/<your-user>/A-Puzzle-A-Day-solver.git
cd A-Puzzle-A-Day-solver

python apuzzle_solver.py July 6     # spelled-out month
python apuzzle_solver.py 7 6        # numeric month
