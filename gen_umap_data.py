"""
Generates synthetic cerebellar-cell-type 2D embedding data with a hierarchy
that splits at specific, fixed clustering resolutions:

  0.4  -> 4 clusters:  Purkinje Cells, Interneurons, Astrocytes, Ependymal
  0.5  -> 6 clusters:  Purkinje splits -> Zebrin-Positive / Zebrin-Negative
                       Astrocytes splits -> Protoplasmic / Fibrous Astrocytes
                       Interneurons, Ependymal unchanged
  0.8  -> 7 clusters:  Interneurons splits -> MLIs / UBCs
                       all others unchanged
  1.0  -> 7 clusters:  unchanged from 0.8 (plateau step)
  1.2  -> 8 clusters:  Ependymal splits -> E1 / E2 Ependymal Cells
                       all others unchanged

Each parent has ~100 points. Once a parent splits, its points are
permanently divided between the two child leaves (no re-merging as
resolution increases). Sibling leaves are positioned close to their shared
parent's location so that, e.g., MLIs and UBCs stay near each other and
away from the Purkinje-derived clusters.

Output: public/data/umap.json. The frontend does NOT interpolate between
these by resolution value -- the slider snaps to exactly these 5 steps,
and on each change the frontend tweens points from their current rendered
position/color to the new step's precomputed position/color.
"""
import json
import math
import random

random.seed(7)

CANVAS = 1000
POINTS_PER_PARENT = 1000

RESOLUTIONS = [0.4, 0.5, 0.8, 1.2]

# split_step = index into RESOLUTIONS at which this parent's points move to
# their two leaf positions/colors/labels.
PARENTS = [
    {
        "id": 0,
        "label": "Purkinje Cells",
        "base_color": "#f2a94e",  # amber
        "split_step": 1,  # splits at resolution 0.5
        "leaves": [
            {"label": "Zebrin-Positive", "color": "#f7c873"},
            {"label": "Zebrin-Negative", "color": "#c97d15"},
        ],
    },
    {
        "id": 1,
        "label": "Interneurons",
        "base_color": "#3ba9a6",  # teal
        "split_step": 2,  # splits at resolution 0.8
        "leaves": [
            {"label": "MLIs", "color": "#6fc9c6"},
            {"label": "UBCs", "color": "#1f6b69"},
        ],
    },
    {
        "id": 2,
        "label": "Astrocytes",
        "base_color": "#e2725b",  # coral
        "split_step": 1,  # splits at resolution 0.5
        "leaves": [
            {"label": "Protoplasmic Astrocytes", "color": "#ee9c8b"},
            {"label": "Fibrous Astrocytes", "color": "#b74a34"},
        ],
    },
    {
        "id": 3,
        "label": "Ependymal",
        "base_color": "#7c8cd6",  # indigo
        "split_step": 3,  # splits at resolution 1.2
        "leaves": [
            {"label": "E1 Ependymal Cells", "color": "#a6b1e6"},
            {"label": "E2 Ependymal Cells", "color": "#4f5fae"},
        ],
    },
]


def polar(cx, cy, r, theta):
    return cx + r * math.cos(theta), cy + r * math.sin(theta)


def gauss_point(cx, cy, spread):
    r = abs(random.gauss(0, spread))
    a = random.uniform(0, 2 * math.pi)
    return polar(cx, cy, r, a)


# --- Parent (super-cluster) centers, spread around the canvas ---
N_PARENTS = len(PARENTS)
parent_centers = []
for i, p in enumerate(PARENTS):
    theta = (2 * math.pi / N_PARENTS) * i + 0.5
    cx, cy = polar(CANVAS / 2, CANVAS / 2, CANVAS * 0.27, theta)
    parent_centers.append((cx, cy))
    p["center"] = (cx, cy)

# --- Leaf centers: two per parent, close to the parent's own center ---
for p in PARENTS:
    pcx, pcy = p["center"]
    base_rot = random.uniform(0, 2 * math.pi)
    for li, leaf in enumerate(p["leaves"]):
        theta = base_rot + li * math.pi  # two leaves, opposite sides
        lcx, lcy = polar(pcx, pcy, CANVAS * 0.075, theta)
        leaf["center"] = (lcx, lcy)

# --- Generate points ---
points = []
for p in PARENTS:
    pcx, pcy = p["center"]
    for i in range(POINTS_PER_PARENT):
        # pre-split "blob" position: single scatter around the parent center
        blob_x, blob_y = gauss_point(pcx, pcy, CANVAS * 0.045)
        leaf_idx = i % 2  # even 50/50 split when it eventually divides
        leaf = p["leaves"][leaf_idx]
        lcx, lcy = leaf["center"]
        final_x, final_y = gauss_point(lcx, lcy, CANVAS * 0.028)
        points.append({
            "parent_id": p["id"],
            "parent_label": p["label"],
            "parent_color": p["base_color"],
            "split_step": p["split_step"],
            "blob_pos": (blob_x, blob_y),
            "final_pos": (final_x, final_y),
            "leaf_label": leaf["label"],
            "leaf_color": leaf["color"],
        })

random.shuffle(points)

# --- Precompute each of the 5 resolution steps ---
steps_out = []
legends_out = []
for step_idx, res in enumerate(RESOLUTIONS):
    step_points = []
    for pt in points:
        if step_idx < pt["split_step"]:
            x, y = pt["blob_pos"]
            color = pt["parent_color"]
            label = pt["parent_label"]
        else:
            x, y = pt["final_pos"]
            color = pt["leaf_color"]
            label = pt["leaf_label"]
        step_points.append([round(x, 2), round(y, 2), color, label])
    steps_out.append(step_points)
    # keep legend ordering stable: parent order, then split status
    ordered_legend = []
    for p in PARENTS:
        if step_idx < p["split_step"]:
            ordered_legend.append({"label": p["label"], "color": p["base_color"]})
        else:
            for leaf in p["leaves"]:
                ordered_legend.append({"label": leaf["label"], "color": leaf["color"]})
    legends_out.append(ordered_legend)

data = {
    "canvasSize": CANVAS,
    "resolutions": RESOLUTIONS,
    "defaultIndex": 1,  # 0.5
    "numPoints": len(points),
    "steps": steps_out,          # steps[stepIndex][pointIndex] = [x, y, color, label]
    "legends": legends_out,      # legends[stepIndex] = [{label, color}, ...]
}

with open("public/data/umap.json", "w") as f:
    json.dump(data, f, separators=(",", ":"))

print(f"Wrote {len(points)} points x {len(RESOLUTIONS)} resolution steps")
for i, res in enumerate(RESOLUTIONS):
    print(f"  {res}: {len(legends_out[i])} clusters -> {[l['label'] for l in legends_out[i]]}")
