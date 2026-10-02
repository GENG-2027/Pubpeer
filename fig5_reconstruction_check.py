#!/usr/bin/env python3
"""
Reproduce the Fig. 5 vector-point check from the published PDF.

Usage:
    python fig5_reconstruction_check.py ARTICLE.pdf

Requirements:
    pip install pymupdf numpy

The script:
1) extracts the 6,400 black filled vector markers from Fig. 5;
2) calibrates the x-axis from the published numerical ticks;
3) preserves PDF drawing order within each model/metric row;
4) reconstructs the plotted performance coordinates using one
   NumPy RandomState sequence initialized with seed 42;
5) reports maximum absolute discrepancy and group-wise correlations.
"""

import sys
import fitz
import numpy as np

if len(sys.argv) != 2:
    raise SystemExit("Usage: python fig5_reconstruction_check.py ARTICLE.pdf")

pdf_path = sys.argv[1]
page = fitz.open(pdf_path)[5]

points = []
for draw_index, d in enumerate(page.get_drawings()):
    r = d["rect"]
    if (
        d.get("type") == "f"
        and d.get("fill") == (0.0, 0.0, 0.0)
        and abs(r.width - 0.92) < 0.02
        and abs(r.height - 0.92) < 0.02
    ):
        points.append({
            "draw_index": draw_index,
            "x": (r.x0 + r.x1) / 2,
            "y": (r.y0 + r.y1) / 2,
        })

assert len(points) == 6400, f"Expected 6400 filled dots, found {len(points)}."

allowed = {"65", "70", "75", "80", "85", "90", "95", "100"}
left_ticks, right_ticks = [], []
for w in page.get_text("words"):
    x0, y0, x1, y1, text, *_ = w
    if 500 < y0 < 525 and text in allowed:
        xc = (x0 + x1) / 2
        (left_ticks if xc < 300 else right_ticks).append((xc, float(text)))

left_coef = np.polyfit(
    [x for x, v in left_ticks], [v for x, v in left_ticks], 1
)
right_coef = np.polyfit(
    [x for x, v in right_ticks], [v for x, v in right_ticks], 1
)

models_top_to_bottom = [
    "BrainGNN", "BNT", "LG-GNN", "Com-brainTF",
    "BrainLM", "TFF", "SwiFT", "NeuroSTORM"
]
groups = {}

for metric, side_points, coef in [
    ("Top-1 accuracy", [p for p in points if p["x"] < 300], left_coef),
    ("mAP", [p for p in points if p["x"] >= 300], right_coef),
]:
    ordered_by_y = sorted(side_points, key=lambda p: p["y"])
    for i, model in enumerate(models_top_to_bottom):
        row = ordered_by_y[i*400:(i+1)*400]
        row = sorted(row, key=lambda p: p["draw_index"])
        groups[(metric, model)] = np.polyval(coef, [p["x"] for p in row])

order = [
    "NeuroSTORM", "SwiFT", "TFF", "BrainLM",
    "Com-brainTF", "LG-GNN", "BNT", "BrainGNN"
]
top1_centres = [93.4, 91.7, 89.8, 90.6, 88.6, 89.1, 85.3, 87.5]
map_centres  = [92.5, 90.1, 87.3, 88.7, 86.9, 87.5, 82.2, 85.5]

np.random.seed(42)
all_abs = []
rs = []

for metric, centres in [
    ("Top-1 accuracy", top1_centres),
    ("mAP", map_centres),
]:
    for model, centre in zip(order, centres):
        expected = np.concatenate([
            np.random.normal(centre, 3, 300),
            np.random.normal(centre, 6, 80),
            centre + np.random.uniform(10, 14, 10),
            centre - np.random.uniform(10, 14, 10),
        ])
        expected = np.clip(expected, 0, 100)
        observed = groups[(metric, model)]
        all_abs.extend(np.abs(observed - expected))
        rs.append(np.corrcoef(observed, expected)[0, 1])

print("Filled dots:", len(points))
print("Groups:", 16)
print("Points per group:", 400)
print("Maximum absolute discrepancy (percentage points):", max(all_abs))
print("Median absolute discrepancy (percentage points):", np.median(all_abs))
print("Minimum group-wise Pearson r:", min(rs))
