import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Patch

COL = {"rule": "#e5e7eb", "ai": "#bfdbfe", "human": "#bbf7d0"}
steps = [
 ("1. Reviewer uploads PDFs, picks category", "rule"),
 ("2. Load criteria for category; snapshot version", "rule"),
 ("3. Extract text; scan for hidden text / injection phrases", "rule"),
 ("4. AI extracts facts + exact quotes + page", "ai"),
 ("5. Verify each quote exists in source text", "rule"),
 ("6. Mandatory checks: licence, WSIB + $5M insurance", "rule"),
 ("7. Weighted scoring from stored facts (code)", "rule"),
 ("8. Rank; flag: injection, missing data, unclear", "rule"),
 ("9. AI writes one-line reasons (wording only)", "ai"),
 ("10. Reviewer checks flags, edits facts, overrides with reason", "human"),
 ("11. Human makes the final award decision", "human"),
]
fig, ax = plt.subplots(figsize=(8, 12))
ax.set_xlim(0, 11.5); ax.set_ylim(0, len(steps) * 1.3 + 1.2); ax.axis("off")
top = len(steps) * 1.3 + 0.6
ys = []
for i, (t, k) in enumerate(steps):
    y = top - i * 1.3 - 0.9; ys.append(y)
    ax.add_patch(FancyBboxPatch((1.2, y), 6.2, 0.85, boxstyle="round,pad=0.05", fc=COL[k], ec="#374151"))
    ax.text(4.3, y + 0.42, t, ha="center", va="center", fontsize=9)
    if i: ax.annotate("", xy=(4.3, y + 0.9), xytext=(4.3, ys[i-1]), arrowprops=dict(arrowstyle="->", color="#374151"))
side = [(5, "Flagged / ineligible\n(B, C, D) -> reviewer"), (9, "Every step logged:\ncriteria + prompt version,\nraw output, scores, overrides")]
ax.text(9.6, ys[5] + 0.4, side[0][1], fontsize=8, ha="center", va="center", color="#991b1b")
ax.annotate("", xy=(8.2, ys[5] + 0.4), xytext=(7.5, ys[5] + 0.4), arrowprops=dict(arrowstyle="<-", color="#991b1b"))
ax.text(9.6, ys[9] - 0.2, side[1][1], fontsize=8, ha="center", va="center", color="#1e3a8a")
ax.legend(handles=[Patch(fc=COL["ai"], ec="#374151", label="AI step"),
                   Patch(fc=COL["rule"], ec="#374151", label="Rule / code step"),
                   Patch(fc=COL["human"], ec="#374151", label="Human checkpoint")],
          loc="lower center", ncol=3, frameon=False)
ax.set_title("AI-assisted proposal triage: upload to ranked output", fontsize=12)
plt.savefig("../diagram/flow.png", dpi=160, bbox_inches="tight")
