import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Fichier supplementaire S1: Ranking of periodic genes from the S. cerevisiae cell cycle
xlsx_path = "pgen.1006453.s002.xlsx"
out_path = "figure_2A_reproduite.png"

# Les deux premières lignes du fichier ne sont pas l'en-tete; l'en-tete est à la ligne 3 du fichier Excel.
df = pd.read_excel(xlsx_path, sheet_name="Sheet1", header=2)

# Les genes utilises dans la Fig. 2A sont ceux qui ont un index dans "Figure2A_order_peaktime".
time_cols = [c for c in df.columns if isinstance(c, (int, float, np.integer, np.floating))]
plot_df = df[df["Figure2A_order_peaktime"].notna()].copy()
plot_df = plot_df.sort_values("Figure2A_order_peaktime")

# Matrice d'expression: lignes = genes, colonnes = temps.
expr = plot_df[time_cols].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)

# Z-score par gene, comme dans la légende: changement relatif a la moyenne de chaque gene.
row_mean = np.nanmean(expr, axis=1, keepdims=True)
row_std = np.nanstd(expr, axis=1, ddof=0, keepdims=True)
row_std[row_std == 0] = np.nan
z = (expr - row_mean) / row_std
z = np.clip(z, -1.5, 1.5)

# Palette proche de la figure originale: faible = cyan, moyen = noir, fort = jaune.
cmap = LinearSegmentedColormap.from_list("cyan_black_yellow", ["#00cfe8", "#111111", "#ffe600"])

fig, ax = plt.subplots(figsize=(3.0, 5.2), dpi=300)
im = ax.imshow(
    z,
    aspect="auto",
    interpolation="nearest",
    cmap=cmap,
    vmin=-1.5,
    vmax=1.5,
    origin="upper",
    extent=[min(time_cols), max(time_cols), z.shape[0], 0],
)

ax.set_title(r"$\it{Saccharomyces\ cerevisiae}$", fontsize=9, pad=6)
ax.set_xlabel("time (minutes)", fontsize=8)
ax.set_ylabel(f"Top Periodic Genes ({z.shape[0]})", fontsize=8)
ax.set_xticks([0, 50, 100, 150, 200])
ax.tick_params(axis="both", labelsize=7, length=2)

cbar = fig.colorbar(im, ax=ax, fraction=0.055, pad=0.035)
cbar.set_ticks([-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5])
cbar.ax.tick_params(labelsize=7, length=2)
cbar.ax.text(1.9, 1.00, "High", transform=cbar.ax.transAxes, fontsize=7, va="top")
cbar.ax.text(1.9, 0.00, "Low", transform=cbar.ax.transAxes, fontsize=7, va="bottom")

fig.tight_layout()
fig.savefig(out_path, bbox_inches="tight")
plt.show()
