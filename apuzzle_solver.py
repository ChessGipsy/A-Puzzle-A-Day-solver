#!/usr/bin/env python3
"""
apuzzle_solver.py  –  calendar-puzzle exact-cover solver
                       (shows tries count and run-time)

examples
    apuzzle_solver.py July 6
    apuzzle_solver.py 7 6
"""

from __future__ import annotations
import sys, argparse, time
from typing import List, Tuple, Dict, Set, Iterable, Optional

# ────────────────────────────── 1.  BOARD ──────────────────────────────
ROW_WIDTHS = [6, 6, 7, 7, 7, 7, 3]
MONTHS     = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]

BOARD_CELLS: List[Tuple[int, int]] = []
CELL_TO_COL: Dict[Tuple[int, int], int] = {}
for r, w in enumerate(ROW_WIDTHS):
    for c in range(w):
        CELL_TO_COL[(r, c)] = len(BOARD_CELLS)
        BOARD_CELLS.append((r, c))

def month_cell(m: int) -> Tuple[int, int]:
    return (0, m - 1) if m <= 6 else (1, m - 7)

def day_cell(d: int) -> Tuple[int, int]:
    if d <= 7:   return (2, d - 1)
    if d <= 14:  return (3, d - 8)
    if d <= 21:  return (4, d - 15)
    if d <= 28:  return (5, d - 22)
    return (6, d - 29)

# ────────────────────────────── 2.  PIECES ─────────────────────────────
RawPiece = List[List[int]]
PIECES: Dict[str, RawPiece] = {
    "A": [[1,0],[1,0],[1,0],[1,1]],
    "B": [[1,0],[1,0],[1,1],[1,0]],
    "C": [[1,0],[1,0],[1,1],[0,1]],
    "D": [[1,1],[1,0],[1,1]],
    "E": [[1,1],[1,1],[1,1]],          # 6 squares
    "F": [[1,0],[1,1],[1,1]],
    "G": [[1,1,0],[0,1,0],[0,1,1]],
    "H": [[1,0,0],[1,0,0],[1,1,1]],
}

CoordSet = Tuple[Tuple[int,int], ...]
Transform = Tuple[CoordSet, int, bool]

def grid_to_coords(g: RawPiece) -> CoordSet:
    return tuple((r, c) for r, row in enumerate(g) for c, v in enumerate(row) if v)

def rotate(cs: CoordSet) -> CoordSet:
    h = max(r for r, _ in cs) + 1
    return tuple((c, h - 1 - r) for r, c in cs)

def flip(cs: CoordSet) -> CoordSet:
    w = max(c for _, c in cs) + 1
    return tuple((r, w - 1 - c) for r, c in cs)

def normalize(cs: CoordSet) -> CoordSet:
    mr = min(r for r, _ in cs)
    mc = min(c for _, c in cs)
    return tuple(sorted((r - mr, c - mc) for r, c in cs))

def all_transforms(g: RawPiece) -> List[Transform]:
    base = grid_to_coords(g)
    seen: Set[CoordSet] = set()
    out: List[Transform] = []
    for flipped in (False, True):
        cs0 = flip(base) if flipped else base
        for rot in (0, 90, 180, 270):
            cs = cs0
            for _ in range(rot // 90):
                cs = rotate(cs)
            ncs = normalize(cs)
            if ncs not in seen:
                seen.add(ncs)
                out.append((ncs, rot, flipped))
    return out

class Placement:
    def __init__(self, piece: str, squares: Iterable[int],
                 top_left: Tuple[int, int], rotation: int, flipped: bool):
        self.piece     = piece
        self.squares   = tuple(sorted(squares))
        self.top_left  = top_left
        self.rotation  = rotation
        self.flipped   = flipped
    def __repr__(self):
        return (f"{self.piece}@{self.top_left} rot{self.rotation}"
                f" flip{self.flipped}")

def generate_placements(excluded: Set[Tuple[int, int]]) -> List[Placement]:
    res: List[Placement] = []
    rows = len(ROW_WIDTHS)
    for name, grid in PIECES.items():
        for coords, rot, fl in all_transforms(grid):
            max_r, max_c = max(r for r, _ in coords), max(c for _, c in coords)
            for tr in range(rows - max_r):
                for tc in range(ROW_WIDTHS[tr] - max_c):
                    ok = True
                    cell_idxs: List[int] = []
                    for pr, pc in coords:
                        r, c = tr + pr, tc + pc
                        if c >= ROW_WIDTHS[r] or (r, c) in excluded:
                            ok = False
                            break
                        cell_idxs.append(CELL_TO_COL[(r, c)])
                    if ok:
                        res.append(Placement(name, cell_idxs, (tr, tc), rot, fl))
    return res

# ──────────────────────────── 3.  EXACT-COVER ───────────────────────────
def solve_exact_cover(placements: List[Placement],
                      excluded: Set[Tuple[int, int]]
                      ) -> Tuple[Optional[List[Placement]], int]:
    """Return (solution, tries). `tries` = number of placement rows considered."""
    board_cols = {CELL_TO_COL[xy] for xy in BOARD_CELLS if xy not in excluded}
    piece_cols = {p: max(board_cols) + 1 + i for i, p in enumerate(sorted(PIECES))}
    universe   = board_cols | set(piece_cols.values())

    col_to_rows: Dict[int, List[int]] = {c: [] for c in universe}
    for idx, pl in enumerate(placements):
        cols = (set(pl.squares) & board_cols) | {piece_cols[pl.piece]}
        for c in cols:
            col_to_rows[c].append(idx)

    sol: List[int] = []
    used: Set[int] = set()
    tries = 0      # counter

    def choose() -> int:
        return min(universe - used, key=lambda c:
                   len([r for r in col_to_rows[c]
                        if not (set(placements[r].squares) & used)]))

    def search() -> bool:
        nonlocal tries
        if used == universe:
            return True
        col = choose()
        for row in col_to_rows[col]:
            tries += 1
            row_cols = (set(placements[row].squares) & board_cols) | \
                       {piece_cols[placements[row].piece]}
            if row_cols & used:
                continue
            sol.append(row)
            used.update(row_cols)
            if search():
                return True
            sol.pop()
            used.difference_update(row_cols)
        return False

    found = search()
    return ([placements[r] for r in sol] if found else None, tries)

# ─────────────────────────── 4.  VISUALISER ────────────────────────────
def show_board(solution: List[Placement], month: int, day: int) -> None:
    board = [["   " for _ in range(w)] for w in ROW_WIDTHS]
    for pl in solution:
        for idx in pl.squares:
            r, c = BOARD_CELLS[idx]
            board[r][c] = f" {pl.piece} "
    mr, mc = month_cell(month); board[mr][mc] = MONTHS[month - 1][:3]
    dr, dc = day_cell(day);     board[dr][dc] = str(day).rjust(3)

    print("\nSolution layout:")
    for row in board:
        print(" ".join(row))

# ─────────────────────────── 5.  ARG-PARSE & MAIN ───────────────────────
def parse_args(argv):
    ap = argparse.ArgumentParser(description="Calendar-puzzle solver")
    ap.add_argument("month", help="Month name (English) or 1-12")
    ap.add_argument("day",   help="Day of month 1-31", type=int)
    a = ap.parse_args(argv)
    month = int(a.month) if a.month.isdigit() \
            else MONTHS.index(a.month.capitalize()) + 1
    if not 1 <= month <= 12 or not 1 <= a.day <= 31:
        sys.exit("Invalid date")
    return month, a.day

def main(argv):
    month, day = parse_args(argv)
    exposed = {month_cell(month), day_cell(day)}

    t0 = time.perf_counter()
    placements = generate_placements(exposed)
    solution, tries = solve_exact_cover(placements, exposed)
    elapsed = time.perf_counter() - t0

    if solution is None:
        print("No solution.")
        print(f"Tries: {tries}")
        print(f"Time:  {elapsed:.3f} s")
        return

    # 1) structured machine-readable answer
    structured = [{"piece": p.piece, "row": p.top_left[0], "col": p.top_left[1],
                   "rotation": p.rotation, "flipped": p.flipped}
                  for p in sorted(solution, key=lambda x: x.piece)]
    print(structured)

    # 2) pretty board
    show_board(solution, month, day)

    # 3) stats
    print(f"\nTries: {tries}")
    print(f"Time:  {elapsed:.3f} s")

if __name__ == "__main__":
    main(sys.argv[1:])
