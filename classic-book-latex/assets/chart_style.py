"""Matplotlib setup for charts that match the page. Usage:
    import chart_style; fig, ax = chart_style.figure(height=2.5)
    ...; fig.savefig("chart.pdf")"""
import subprocess, matplotlib as mpl
from matplotlib import font_manager as fm, pyplot as plt

for _f in ("regular", "italic", "bold"):
    fm.fontManager.addfont(subprocess.check_output(
        ["kpsewhich", f"texgyretermes-{_f}.otf"], text=True).strip())
mpl.rcParams.update({
    "font.family": "TeX Gyre Termes", "font.size": 9,
    "axes.linewidth": .5, "axes.edgecolor": "black",
    "axes.spines.top": False, "axes.spines.right": False,
    "xtick.major.width": .5, "ytick.major.width": .5,
    "xtick.major.size": 3, "ytick.major.size": 3,
    "lines.linewidth": 1.1, "axes.grid": False,
    "axes.prop_cycle": mpl.cycler(color=["black", "0.45", "0.7"]),
    "pdf.fonttype": 42, "savefig.transparent": True,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})

def figure(height=2.5, width=4.5):
    """width 4.5 in = the full 27 pc measure, so type is never rescaled."""
    return plt.subplots(figsize=(width, height))
