import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images") + os.sep

# ---------------- Gantt chart ----------------
tasks = [
    ("1. Research and scoping", 1, 1, "#1f4e79"),
    ("2. Data acquisition and governance review", 1, 2, "#1f4e79"),
    ("3. Exploratory analysis and cleaning", 2, 2, "#2e75b6"),
    ("4. Feature engineering", 3, 2, "#2e75b6"),
    ("5. Baseline models", 4, 1, "#2e75b6"),
    ("6. Advanced model training and tuning", 5, 2, "#c55a11"),
    ("7. Evaluation and error analysis", 7, 1, "#c55a11"),
    ("8. Explainability and ethics review", 7, 2, "#7f6000"),
    ("9. Prototype dashboard and deployment", 8, 2, "#548235"),
    ("10. Documentation and final report", 9, 2, "#548235"),
]
milestones = [(1, "M1 Plan approved"), (3, "M2 Clean dataset"), (4, "M3 Baseline"),
              (6, "M4 Tuned model"), (8, "M5 Prototype"), (10, "M6 Final delivery")]

fig, ax = plt.subplots(figsize=(11, 5.6))
n = len(tasks)
for i, (name, start, dur, col) in enumerate(tasks):
    y = n - i
    ax.barh(y, dur, left=start - 1, height=0.55, color=col, edgecolor="white")
    ax.text(start - 1 + dur / 2, y, f"W{start}" if dur == 1 else f"W{start}-W{start+dur-1}",
            ha="center", va="center", color="white", fontsize=8, fontweight="bold")
ax.set_yticks([n - i for i in range(n)])
ax.set_yticklabels([t[0] for t in tasks], fontsize=9)
ax.set_xticks([i + 0.5 for i in range(10)])
ax.set_xticklabels([f"W{i+1}" for i in range(10)], fontsize=9)
ax.set_xlim(0, 10.4)
ax.set_ylim(0, n + 1.9)
for x in range(11):
    ax.axvline(x, color="#dddddd", lw=0.6, zorder=0)
for k, (wk, label) in enumerate(milestones):
    x = wk
    ax.plot([x], [n + 0.75], marker="D", color="#c00000", markersize=8, zorder=5)
    ax.text(x - 0.05, n + 1.2 + (0.35 if k % 2 else 0), label, ha="right" if x > 1 else "left",
            fontsize=8, color="#c00000")
ax.set_title("AirCast India - 10-Week Project Timeline (Gantt Chart)", fontsize=12, fontweight="bold", loc="left")
ax.set_xlabel("Project week (end-of-week markers show milestones)", fontsize=9)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
plt.tight_layout()
plt.savefig(OUT + "gantt.png", dpi=200)
plt.close()

# ---------------- Workflow diagram ----------------
steps = ["Public data\n(CPCB, ERA5,\nFIRMS)", "Ingest and\nvalidate", "Clean and\nimpute", "Feature\nengineering",
         "Model training\nand tuning", "Evaluation and\nexplainability", "Dashboard\nand monitoring"]
fig, ax = plt.subplots(figsize=(11, 2.6))
ax.set_xlim(0, 11)
ax.set_ylim(-0.6, 2.2)
ax.axis("off")
w, h, gap = 1.33, 1.2, 0.27
x0 = 0.1
cols = ["#1f4e79", "#2e75b6", "#2e75b6", "#2e75b6", "#c55a11", "#7f6000", "#548235"]
for i, s in enumerate(steps):
    x = x0 + i * (w + gap)
    ax.add_patch(FancyBboxPatch((x, 0.7), w, h, boxstyle="round,pad=0.03", fc=cols[i], ec="none"))
    ax.text(x + w / 2, 0.7 + h / 2, s, ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    if i < len(steps) - 1:
        ax.add_patch(FancyArrowPatch((x + w + 0.03, 1.3), (x + w + gap - 0.03, 1.3), arrowstyle="-|>",
                                     mutation_scale=12, color="#444444"))
# feedback loop
ax.add_patch(FancyArrowPatch((x0 + 6 * (w + gap) + w / 2, 0.65), (x0 + 3 * (w + gap) + w / 2, 0.65),
                             connectionstyle="arc3,rad=-0.3", arrowstyle="-|>", mutation_scale=12,
                             color="#c00000", ls="--"))
ax.text(x0 + 4.5 * (w + gap), -0.5, "Feedback loop: drift detection and error analysis trigger re-engineering/retraining",
        ha="center", fontsize=8, color="#c00000")
plt.savefig(OUT + "workflow.png", dpi=200, bbox_inches="tight")
plt.close()
print("done")
