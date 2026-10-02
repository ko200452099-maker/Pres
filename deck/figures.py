"""
Figures for Seminar_FormationDamage — drawn at their true on-slide size so that
in-figure type renders at its nominal point size (axis labels 16-18 pt).

Palette follows the design system:
  navy   #0B2545  titles / structure
  teal   #13828C  healthy / ideal
  amber  #F28C28  highlights, "look here"
  red    #C0392B  damage only
  charcoal #2E2E2E body text
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Polygon, FancyBboxPatch

NAVY = "#0B2545"
TEAL = "#13828C"
AMBER = "#F28C28"
RED = "#C0392B"
CHAR = "#2E2E2E"
GREY = "#5A6472"
LGREY = "#C8D0D9"
PANEL = "#EEF1F5"
TEALP = "#E3F0F1"
REDP = "#F9E9E7"
WHITE = "#FFFFFF"
BORDER = "#D8DEE5"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 16,
    "axes.edgecolor": GREY,
    "axes.labelcolor": CHAR,
    "axes.labelsize": 17,
    "axes.titlesize": 17,
    "xtick.color": CHAR,
    "ytick.color": CHAR,
    "xtick.labelsize": 16,
    "ytick.labelsize": 16,
    "legend.frameon": False,
    "savefig.facecolor": WHITE,
    "figure.facecolor": WHITE,
})

# ---- reservoir constants (verified in calc.py)
k, ks, h, rw, re, rs = 100.0, 20.0, 50.0, 0.354, 745.0, 3.0
mu, B, pbar, pwf = 1.0, 1.2, 3500.0, 2500.0
DP = pbar - pwf
GEOM = math.log(re / rw) - 0.75
S_DAM = (k / ks - 1) * math.log(rs / rw)
J0 = 0.00708 * k * h / (mu * B * GEOM)
JD = 0.00708 * k * h / (mu * B * (GEOM + S_DAM))
Q0, QD = J0 * DP, JD * DP
FE_DAM = JD / J0
OUT = "figures/"


def clean(ax, grid="y"):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    if grid:
        ax.grid(axis=grid, color=LGREY, lw=0.8, alpha=0.6, zorder=0)
        ax.set_axisbelow(True)


def save(fig, name, transparent=False):
    fig.savefig(OUT + name, dpi=300, transparent=transparent)
    plt.close(fig)
    print("  wrote", name)


def thousands(ax, axis="x"):
    from matplotlib.ticker import FuncFormatter
    f = FuncFormatter(lambda v, p: f"{v:,.0f}")
    (ax.xaxis if axis == "x" else ax.yaxis).set_major_formatter(f)


# ================================================================ S2  IPR (two layers)
S2_FIG = (12.1, 4.55)
S2_RECT = [0.078, 0.175, 0.885, 0.79]


def _ipr_axes(with_damage):
    fig = plt.figure(figsize=S2_FIG)
    ax = fig.add_axes(S2_RECT)
    qmax = 9000
    q = np.array([0, qmax])
    if not with_damage:
        ax.plot(q, pbar - q / J0, color=TEAL, lw=4.0, solid_capstyle="round",
                zorder=3)
        # manual legend entry (so the damaged entry can appear with the overlay)
        ax.plot([0.62, 0.68], [0.935, 0.935], transform=ax.transAxes, color=TEAL,
                lw=4.0, clip_on=False, zorder=6)
        ax.text(0.695, 0.935, "$\\mathbf{J}$ = 4.27 STB/d/psi", transform=ax.transAxes,
                fontsize=16, color=TEAL, va="center", fontweight="bold", zorder=6)
        ax.text(0.695, 0.855, "Undamaged (S = 0)", transform=ax.transAxes,
                fontsize=16, color=CHAR, va="center", zorder=6)
        ax.plot([Q0], [2500], "o", ms=11, mfc=WHITE, mec=TEAL, mew=3.0, zorder=5)
        ax.text(Q0, 2620, "4,270", ha="center", va="bottom", fontsize=18,
                fontweight="bold", color=TEAL, zorder=6,
                bbox=dict(fc=WHITE, ec="none", pad=1.5, alpha=0.9))
        # drawdown arrow
        ax.annotate("", xy=(8560, 2500), xytext=(8560, 3500),
                    arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.6), zorder=2)
        ax.text(8420, 3000, "Drawdown\n1,000 psi", ha="right", va="center",
                fontsize=16, color=CHAR, linespacing=1.3)
        ax.axhline(2500, color=GREY, lw=1.2, ls=(0, (3, 4)), zorder=1)
        ax.text(0.02, 0.055, "Same reservoir, same 1,000 psi drawdown — only skin differs.",
                transform=ax.transAxes, fontsize=16, color=GREY, style="italic")
    else:
        ax.plot(q, pbar - q / JD, color=RED, lw=4.0, ls=(0, (6, 3.5)),
                solid_capstyle="round", zorder=4)
        ax.plot([0.62, 0.68], [0.825, 0.825], transform=ax.transAxes, color=RED,
                lw=4.0, ls=(0, (6, 3.5)), clip_on=False, zorder=6)
        ax.text(0.695, 0.825, "$\\mathbf{J}$ = 1.91 STB/d/psi", transform=ax.transAxes,
                fontsize=16, color=RED, va="center", fontweight="bold", zorder=6)
        ax.text(0.695, 0.745, "Damaged (S = 8.55)", transform=ax.transAxes,
                fontsize=16, color=CHAR, va="center", zorder=6)
        ax.plot([QD], [2500], "o", ms=11, mfc=WHITE, mec=RED, mew=3.0, zorder=5)
        ax.text(QD, 2380, "1,910", ha="center", va="top", fontsize=18,
                fontweight="bold", color=RED, zorder=6,
                bbox=dict(fc=WHITE, ec="none", pad=1.5, alpha=0.9))
    ax.set_xlim(0, qmax)
    ax.set_ylim(1500, 3500)
    ax.set_xlabel("Oil rate, q (STB/d)")
    ax.set_ylabel("Flowing bottomhole pressure, $p_{wf}$ (psi)")
    ax.set_yticks([1500, 2000, 2500, 3000, 3500])
    ax.set_xticks([0, 1500, 3000, 4500, 6000, 7500, 9000])
    thousands(ax)
    thousands(ax, "y")
    clean(ax, grid="both")
    return fig


def fig_s2():
    save(_ipr_axes(False), "s2_ipr_base.png")
    save(_ipr_axes(True), "s2_ipr_dmg.png", transparent=True)


# ================================================================ S5  radial + profile
def fig_s5():
    fig = plt.figure(figsize=(7.0, 4.7))
    ax = fig.add_axes([0.05, 0.60, 0.90, 0.36])
    ax.set_aspect("equal")
    ax.add_patch(Circle((0, 0), 1.0, fc=TEALP, ec=NAVY, lw=2.0, zorder=1))
    for a in np.linspace(0, 2 * np.pi, 22, endpoint=False):
        ax.plot([0.09 * math.cos(a), math.cos(a)], [0.09 * math.sin(a), math.sin(a)],
                color=TEAL, lw=1.6, alpha=0.9, zorder=2)
        ax.annotate("", xy=(math.cos(a) * 0.68, math.sin(a) * 0.68),
                    xytext=(math.cos(a) * 0.80, math.sin(a) * 0.80),
                    arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.6,
                                    mutation_scale=13), zorder=3)
    ax.add_patch(Circle((0, 0), 0.09, fc=WHITE, ec=NAVY, lw=2.4, zorder=4))
    ax.annotate("$r_w$ = 0.354 ft", xy=(-0.60, 0.66), xytext=(-1.70, 0.78),
                fontsize=15, color=CHAR, ha="left", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
    ax.annotate("$r_e$ = 745 ft", xy=(0.71, -0.71), xytext=(1.02, -1.10),
                fontsize=15, color=CHAR, ha="left", va="center", zorder=6,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))
    ax.text(0, 1.60, "Top view: flow converges on the well", ha="center",
            fontsize=16, color=CHAR)
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.55, 1.90)
    ax.axis("off")

    ax2 = fig.add_axes([0.135, 0.135, 0.845, 0.375])
    r = np.logspace(math.log10(rw), math.log10(re), 400)
    p = pbar - DP * (np.log(re / r)) / GEOM
    ax2.plot(r, p, color=TEAL, lw=3.6, zorder=3)
    ax2.fill_between(r, p, 1500, color=TEAL, alpha=0.08, zorder=1)
    ax2.axvline(rw, color=RED, lw=1.8, ls=(0, (4, 3)), zorder=2)
    ax2.text(rw * 1.25, 1580, "$r_w$", color=RED, fontsize=16, va="bottom")
    p3 = pbar - DP * math.log(re / 3.0) / GEOM
    ax2.plot([3.0], [p3], "o", ms=9, mfc=WHITE, mec=RED, mew=2.4, zorder=6)
    ax2.annotate("Steep drop near $r_w$:\n≈ 30% of drawdown\nwithin 3 ft",
                 xy=(3.0, p3), xytext=(26.0, 1720), fontsize=15, color=RED,
                 ha="left", va="bottom", linespacing=1.35, zorder=6,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.4,
                                 connectionstyle="arc3,rad=0.22"))
    ax2.set_xscale("log")
    ax2.set_xlim(0.3, 800)
    ax2.set_ylim(1500, 3500)
    ax2.set_xlabel("Radial distance, r (ft) — log scale")
    ax2.set_ylabel("Pressure (psi)")
    ax2.set_yticks([1500, 2000, 2500, 3000, 3500])
    clean(ax2, grid="both")
    save(fig, "s5_radial.png")


# ================================================================ S6  pressure profile
def fig_s6():
    fig = plt.figure(figsize=(7.0, 4.05))
    ax = fig.add_axes([0.115, 0.175, 0.83, 0.79])
    r = np.logspace(math.log10(rw), math.log10(re), 500)
    C = DP / GEOM
    p_ideal = pwf + C * np.log(r / rw)
    p_skin = np.where(r <= rs, pwf + C * (k / ks) * np.log(r / rw),
                      pwf + C * (math.log(rs / rw) * (k / ks) + np.log(r / rs)))
    ax.plot(r, p_ideal, color=TEAL, lw=3.6, label="Ideal (S = 0)", zorder=3)
    ax.plot(r, p_skin, color=RED, lw=3.6, label="With skin (S = 8.55)", zorder=4)
    ax.fill_between(r, p_ideal, p_skin, where=(r <= rs), color=AMBER, alpha=0.30,
                    zorder=2)
    ax.axvline(rs, color=GREY, lw=1.4, ls=(0, (3, 3)), zorder=1)
    ax.text(0.72, 2452, "$\\Delta p_{skin}$ = 553 psi", fontsize=17,
            color="#B3680E", ha="left", va="bottom", fontweight="bold", zorder=7)
    ax.annotate("", xy=(rw * 1.14, pwf), xytext=(rw * 1.14, pwf + S_DAM * C),
                arrowprops=dict(arrowstyle="<->", color=AMBER, lw=3.0), zorder=6)
    ax.annotate("damaged zone\n($r_s$ = 3 ft)", xy=(rs, 3310), xytext=(14.0, 3480),
                fontsize=15, color=GREY, ha="left", va="center", linespacing=1.35,
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3))
    ax.set_xscale("log")
    ax.set_xlim(0.3, 800)
    ax.set_ylim(2400, 3600)
    ax.set_xlabel("Distance from well, r (ft) — log scale")
    ax.set_ylabel("Pressure (psi)")
    ax.set_yticks([2500, 2700, 2900, 3100, 3300, 3500])
    clean(ax, grid="both")
    ax.legend(loc="lower right", fontsize=16, handlelength=2.2, borderaxespad=0.4,
              labelspacing=0.6)
    save(fig, "s6_profile.png")


# ================================================================ S9  invasion
def fig_s9():
    fig = plt.figure(figsize=(7.0, 4.7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.6)
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 10, 6.6, fc=TEALP, ec="none"))
    ax.add_patch(Rectangle((2.35, 0), 2.6, 6.6, fc=REDP, ec="none"))
    for yy in np.arange(-0.4, 6.9, 0.42):
        ax.plot([2.35, 4.95], [yy, yy + 0.9], color=RED, lw=0.9, alpha=0.45)
    ax.add_patch(Rectangle((2.05, 0), 0.30, 6.6, fc="#C9A227", ec="none"))
    ax.add_patch(Rectangle((0.35, 0), 1.70, 6.6, fc="#BBD3E4", ec=NAVY, lw=1.6))
    ax.text(1.2, 5.6, "Wellbore", rotation=90, ha="center", va="center",
            fontsize=17, color=NAVY, fontweight="bold")
    for yy in (1.6, 3.5, 5.2):
        ax.annotate("", xy=(2.62, yy), xytext=(2.1, yy),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8,
                                    mutation_scale=15))
    ax.annotate("", xy=(4.35, 2.55), xytext=(3.15, 2.55),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8,
                                mutation_scale=15))
    ax.text(5.25, 6.05, "Virgin formation", fontsize=17, color=TEAL,
            fontweight="bold")
    ax.text(3.63, 0.40, "Invaded zone\n(filtrate + solids)", fontsize=16,
            color=RED, ha="center", va="bottom", fontweight="bold", linespacing=1.3)
    ax.annotate("Mud cake", xy=(2.20, 1.15), xytext=(0.12, 0.55), fontsize=16,
                color="#8C6D10", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#8C6D10", lw=1.4))
    ax.add_patch(Rectangle((5.5, 3.30), 4.3, 1.95, fc=WHITE, ec=AMBER, lw=2.0))
    ax.text(7.65, 4.83, "$p_{mud} > p_{formation}$", fontsize=18, color=NAVY,
            ha="center", va="center", fontweight="bold")
    ax.text(7.65, 4.02, "overbalance drives fluid\ninto the rock", fontsize=15,
            color=GREY, ha="center", va="center", linespacing=1.35)
    ax.annotate("", xy=(2.85, 4.20), xytext=(5.4, 4.20),
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.6,
                                connectionstyle="arc3,rad=0.12"))
    save(fig, "s9_invasion.png")


# ================================================================ S10  pore scale
def fig_s10():
    fig = plt.figure(figsize=(7.0, 4.7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.35)
    ax.axis("off")

    def grain(cx, cy, r, label=None, fs=13):
        ax.add_patch(Circle((cx, cy), r, fc="#E9E2D2", ec="#B8A88C", lw=1.4))
        if label:
            ax.text(cx, cy, label, ha="center", va="center", fontsize=fs,
                    color="#7A6A4F")

    ax.text(0.1, 7.05, "Intact pore throat", fontsize=17, color=TEAL,
            fontweight="bold")
    grain(1.9, 5.35, 1.10, "sand\ngrain")
    grain(4.5, 5.35, 1.10, "sand\ngrain")
    grain(1.9, 3.35, 1.10)
    grain(4.5, 3.35, 1.10)
    ax.add_patch(Polygon([[2.70, 5.60], [3.70, 5.60], [3.70, 3.10], [2.70, 3.10]],
                         closed=True, fc="#E3F0F1", ec=TEAL, lw=1.4))
    ax.text(3.2, 4.35, "pore\nthroat", fontsize=15, color=TEAL, ha="center",
            va="center", linespacing=1.25, fontweight="bold")
    ax.add_patch(Circle((3.05, 5.62), 0.32, fc="#8E6BB0", ec="#5E4479", lw=1.3,
                        zorder=4))
    ax.annotate("Bridging particle ≈ ⅓ of throat", xy=(3.05, 5.94),
                xytext=(3.35, 6.72), fontsize=15, color="#5E4479", ha="left",
                va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#5E4479", lw=1.4))
    grain(7.1, 5.35, 1.10)
    grain(9.1, 5.35, 1.10)
    ax.add_patch(Circle((8.1, 5.68), 0.36, fc="#8E6BB0", ec="#5E4479", lw=1.3,
                        zorder=4))
    ax.plot([0.1, 9.9], [2.85, 2.85], color=LGREY, lw=1.4, ls=(0, (4, 3)))
    ax.text(0.1, 2.45, "Fines migration blocks the throat", fontsize=17,
            color=RED, fontweight="bold")
    grain(1.6, 1.25, 1.05)
    grain(3.6, 1.25, 1.05)
    ax.add_patch(Polygon([[2.28, 1.60], [2.92, 1.60], [2.92, 0.65], [2.28, 0.65]],
                         closed=True, fc=REDP, ec=RED, lw=1.3))
    ax.text(2.60, 1.15, "blocked", fontsize=13, color=RED, rotation=90,
            ha="center", va="center", fontweight="bold")
    for (sx, sy), (ex, ey) in (((6.8, 2.25), (3.95, 1.48)),
                               ((7.6, 2.05), (4.00, 1.10)),
                               ((8.5, 2.30), (4.05, 1.30))):
        ax.annotate("", xy=(ex, ey), xytext=(sx, sy),
                    arrowprops=dict(arrowstyle="-|>", color="#5E4479", lw=1.8,
                                    mutation_scale=14))
        ax.add_patch(Circle((sx, sy), 0.15, fc="#8E6BB0", ec="#5E4479", lw=1.0))
    ax.text(7.4, 0.82, "migrating fines", fontsize=15, color="#5E4479",
            ha="center", fontweight="bold")
    grain(6.0, 1.25, 1.05)
    grain(8.4, 1.25, 1.05)
    save(fig, "s10_solids.png")


# ================================================================ S12  capillary
def fig_s12():
    fig = plt.figure(figsize=(7.0, 4.0))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.7)
    ax.axis("off")
    for cx in (1.45, 4.45):
        ax.add_patch(Circle((cx, 2.9), 1.55, fc="#E9E2D2", ec="#B8A88C", lw=1.6))
    ax.plot([2.95, 2.95], [4.45, 1.35], color="#8C7A5C", lw=2.6,
            solid_capstyle="round")
    for cx in (2.25, 3.65):
        ax.add_patch(Circle((cx, 2.9), 0.66, fc="#4A90C4", ec="#1F5C87", lw=1.8,
                            zorder=4, alpha=0.93))
        ax.text(cx, 2.9, "H$_2$O", color=WHITE, fontsize=15, ha="center",
                va="center", fontweight="bold", zorder=5)
    ax.annotate("Trapped water drops\nblock the pore throat", xy=(3.65, 3.60),
                xytext=(5.40, 4.45), fontsize=16, color="#1F5C87", linespacing=1.3,
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#1F5C87", lw=1.5))
    ax.annotate("", xy=(1.70, 2.9), xytext=(0.20, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.6,
                                mutation_scale=18))
    ax.text(0.20, 3.55, "oil", fontsize=16, color=TEAL, fontweight="bold")
    ax.annotate("", xy=(8.45, 2.9), xytext=(6.15, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=LGREY, lw=2.6,
                                mutation_scale=18, alpha=0.8))
    ax.text(7.30, 3.45, "no flow", fontsize=16, color=GREY, fontweight="bold",
            ha="center")
    ax.add_patch(Rectangle((5.65, 0.30), 4.1, 1.45, fc=WHITE, ec=AMBER, lw=2.0))
    ax.text(7.70, 1.02, "small r  →  high $P_c$", fontsize=19, color=NAVY,
            ha="center", va="center", fontweight="bold")
    save(fig, "s12_capillary.png")


# ================================================================ S13  precipitates
def fig_s13():
    fig = plt.figure(figsize=(7.0, 4.7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.7)
    ax.axis("off")
    # header: the two incompatible waters meet
    ax.add_patch(Rectangle((0.30, 5.45), 2.45, 0.85, fc=TEALP, ec=TEAL, lw=1.8))
    ax.text(1.52, 5.87, "SO$_4^{2-}$  filtrate", fontsize=15, color=TEAL,
            ha="center", va="center", fontweight="bold")
    ax.add_patch(Rectangle((7.25, 5.45), 2.45, 0.85, fc=PANEL, ec=NAVY, lw=1.8))
    ax.text(8.47, 5.87, "Ba$^{2+}$  brine", fontsize=15, color=NAVY,
            ha="center", va="center", fontweight="bold")
    ax.annotate("", xy=(4.35, 5.88), xytext=(2.95, 5.88),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.8,
                                mutation_scale=16))
    ax.annotate("", xy=(5.65, 5.88), xytext=(7.05, 5.88),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.8,
                                mutation_scale=16))
    ax.text(5.0, 5.87, "mix", fontsize=15, color=GREY, ha="center", va="center")
    # the pore
    for (cx, cy, r) in ((1.45, 2.85, 1.75), (5.15, 2.85, 1.75)):
        ax.add_patch(Circle((cx, cy), r, fc="#E9E2D2", ec="#B8A88C", lw=1.6))
    ax.add_patch(Polygon([[3.00, 4.45], [3.00, 1.25], [6.85, 1.25], [6.85, 4.45]],
                         closed=True, fc="#E3F0F1", ec=TEAL, lw=1.4, zorder=1))
    for (cx, cy, w, h, ang) in ((3.75, 2.05, 0.72, 0.34, 20),
                                (5.00, 2.85, 0.82, 0.32, -15),
                                (5.95, 1.55, 0.65, 0.30, 35),
                                (4.35, 1.35, 0.70, 0.28, -5),
                                (5.75, 3.75, 0.62, 0.28, 10)):
        ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h, angle=ang, fc=WHITE,
                               ec=RED, lw=1.8, zorder=4))
    ax.annotate("BaSO$_4$ crystals plug the pore", xy=(6.85, 3.55),
                xytext=(7.35, 4.55), fontsize=16, color=RED, ha="right",
                va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
    ax.add_patch(Rectangle((0.30, 0.28), 9.40, 0.88, fc=PANEL, ec="none"))
    ax.text(5.0, 0.72, "Scale nucleates where the two waters meet", fontsize=16,
            color=CHAR, ha="center", va="center")
    save(fig, "s13_precip.png")


# ================================================================ S14  buildup
def fig_s14():
    fig = plt.figure(figsize=(6.0, 4.5))
    ax = fig.add_axes([0.155, 0.185, 0.775, 0.78])
    x = np.linspace(0, 3.0, 200)
    p = 3050 + 105 * x - 8 * np.clip(x - 2.4, 0, None) ** 2 * 6
    ax.plot(10 ** x, p, color=NAVY, lw=4.0, zorder=3)
    xs = np.array([0, 1.25])
    ax.plot(10 ** xs, 3050 + 105 * xs, color=NAVY, lw=1.8, ls=(0, (4, 3)), zorder=2)
    ax.annotate("", xy=(10 ** 1.85, 3050 + 105 * 1.85),
                xytext=(10 ** 1.85, 3050 + 105 * 1.15),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.0))
    ax.annotate("", xy=(10 ** 1.15, 3050 + 105 * 1.15),
                xytext=(10 ** 1.85, 3050 + 105 * 1.15),
                arrowprops=dict(arrowstyle="<->", color=RED, lw=2.0))
    ax.text(10 ** 1.5, 3050 + 105 * 0.98, "1 log cycle", fontsize=15, color=RED,
            ha="center", va="top")
    ax.text(10 ** 2.05, 3050 + 105 * 1.5, "Slope → kh", fontsize=16, color=RED,
            ha="left", va="center", fontweight="bold")
    ax.plot([1], [3050], "o", ms=10, mfc=WHITE, mec=AMBER, mew=3.0, zorder=5)
    ax.annotate("Intercept → skin", xy=(1, 3050), xytext=(1.22, 2762), fontsize=16,
                color="#B3680E", ha="left", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=AMBER, lw=1.6))
    ax.set_xscale("log")
    ax.set_xlim(1, 1000)
    ax.set_ylim(2700, 3560)
    ax.set_xticks([1, 10, 100, 1000])
    ax.set_xticklabels(["1", "10", "100", "1,000"])
    ax.set_xlabel("Horner time, log[$(t_p+\\Delta t)/\\Delta t$]")
    ax.set_ylabel("$p_{ws}$ (psi)")
    clean(ax, grid="both")
    save(fig, "s14_buildup.png")


# ================================================================ S15  Hawkins cylinder
def fig_s15():
    fig = plt.figure(figsize=(3.7, 3.5))
    ax = fig.add_axes([0.02, 0.03, 0.96, 0.92])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(Circle((0, 0), 1.00, fc=TEALP, ec=TEAL, lw=2.2))
    ax.add_patch(Circle((0, 0), 0.62, fc=REDP, ec=RED, lw=2.2))
    for a in np.arange(0, 2 * math.pi, math.pi / 14):
        ax.plot([0.62 * math.cos(a), 1.0 * math.cos(a)],
                [0.62 * math.sin(a), 1.0 * math.sin(a)], color=TEAL, lw=1.0,
                alpha=0.55)
    ax.add_patch(Circle((0, 0), 0.21, fc=WHITE, ec=NAVY, lw=2.4))
    ax.text(0.0, -0.33, "$r_w$", fontsize=14, color=NAVY, ha="center",
            fontweight="bold")
    ax.annotate("$r_s$ = 3 ft", xy=(-0.44, 0.44), xytext=(-1.22, 0.80),
                fontsize=15, color=RED, ha="center", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    ax.annotate("$k_s$ damaged", xy=(0.0, 0.42), xytext=(-1.00, -0.60),
                fontsize=15, color=RED, ha="center", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    ax.annotate("$k$ undamaged", xy=(0.64, -0.62), xytext=(0.98, -1.06),
                fontsize=15, color=TEAL, ha="center", va="center", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.4))
    ax.set_xlim(-1.35, 1.55)
    ax.set_ylim(-1.30, 1.15)
    save(fig, "s15_hawkins.png")


# ================================================================ S16  bars (no callout)
def fig_s16():
    fig = plt.figure(figsize=(6.0, 4.5))
    ax = fig.add_axes([0.16, 0.165, 0.815, 0.70])
    vals = [4270, 1910]
    bars = ax.bar([0, 1], vals, width=0.5, color=[TEAL, RED], zorder=3)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 140, f"{v:,.0f}", ha="center",
                fontsize=21, fontweight="bold", color=b.get_facecolor())
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["Undamaged\n(S = 0)", "Damaged\n(S = 8.55)"], fontsize=16)
    ax.set_ylabel("Oil rate, q (STB/d)")
    ax.set_ylim(0, 5900)
    ax.set_yticks([0, 1000, 2000, 3000, 4000, 5000])
    thousands(ax, "y")
    clean(ax, grid="y")
    ax.tick_params(axis="x", length=0)
    yb = 5100
    ax.plot([0, 0, 1, 1], [4900, yb, yb, 4900], color=GREY, lw=1.4, zorder=4)
    save(fig, "s16_bars.png")


# ================================================================ S17  FE curves
def fig_s17():
    fig = plt.figure(figsize=(6.0, 4.5))
    ax = fig.add_axes([0.145, 0.175, 0.79, 0.765])
    rs_v = np.linspace(0.7, 6.0, 250)
    for kk, c, lab in ((2, TEAL, "$k/k_s$ = 2"), (5, NAVY, "$k/k_s$ = 5"),
                       (10, RED, "$k/k_s$ = 10")):
        S = (kk - 1) * np.log(rs_v / rw)
        ax.plot(rs_v, GEOM / (GEOM + S), color=c, lw=3.8, zorder=3)
        ax.text(6.18, GEOM / (GEOM + (kk - 1) * math.log(6.0 / rw)), lab, color=c,
                fontsize=16, va="center", fontweight="bold")
    ax.plot([3.0, 5.0], [GEOM / (GEOM + 4 * math.log(3 / rw)),
                         GEOM / (GEOM + 4 * math.log(5 / rw))], "o", ms=11,
            mfc=WHITE, mec=NAVY, mew=2.8, zorder=5)
    ax.annotate("3 → 5 ft:\n0.45 → 0.39", xy=(4.0, GEOM / (GEOM + 4 * math.log(4 / rw))),
                xytext=(1.9, 0.60), fontsize=15, color=NAVY, linespacing=1.3,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))
    ax.set_xlim(0.6, 7.7)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([1, 2, 3, 4, 5, 6])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xlabel("Damage radius, $r_s$ (ft)")
    ax.set_ylabel("Flow efficiency, FE (–)")
    clean(ax, grid="both")
    save(fig, "s17_fe.png")


# ================================================================ S18  filter cake
def fig_s18():
    fig = plt.figure(figsize=(7.0, 4.7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.7)
    ax.axis("off")

    def panel(x0, title, cake, invasion, colour, note):
        ax.add_patch(Rectangle((x0, 0.45), 4.35, 5.90, fc=WHITE, ec=colour, lw=2.6))
        ax.text(x0 + 2.18, 5.92, title, fontsize=16, color=colour, ha="center",
                fontweight="bold")
        ax.add_patch(Rectangle((x0 + 1.25, 1.60), 2.95, 3.85, fc=TEALP, ec="none",
                               zorder=1))
        ax.add_patch(Rectangle((x0 + 1.25, 1.60), invasion, 3.85, fc=REDP, ec="none",
                               zorder=2))
        ax.add_patch(Rectangle((x0 + 1.25 - cake, 1.60), cake, 3.85, fc="#C9A227",
                               ec="none", zorder=3))
        ax.add_patch(Rectangle((x0 + 0.30, 1.60), 0.95, 3.85, fc="#BBD3E4", ec=NAVY,
                               lw=1.4, zorder=4))
        ax.text(x0 + 0.775, 3.52, "well", rotation=90, fontsize=13, color=NAVY,
                ha="center", va="center", zorder=5)
        ax.text(x0 + 2.18, 1.00, note, fontsize=15, color=colour, ha="center",
                va="center", fontweight="bold")

    panel(0.15, "Good: thin, tough cake", 0.16, 0.70, TEAL,
          "shallow invasion → low skin")
    panel(5.45, "Poor: thick cake", 0.46, 2.05, RED,
          "deep invasion → high skin")
    ax.annotate("filter cake", xy=(1.33, 4.60), xytext=(2.55, 5.28), fontsize=15,
                color="#8C6D10", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#8C6D10", lw=1.4))
    ax.annotate("invaded zone", xy=(2.35, 2.05), xytext=(3.35, 1.55), fontsize=15,
                color=RED, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    save(fig, "s18_fluids.png")


# ================================================================ S19  decision tree (2 layers)
S19_FIG = (6.0, 4.5)


def _s19(with_branches):
    fig = plt.figure(figsize=S19_FIG)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7.5)
    ax.axis("off")
    if not with_branches:
        ax.add_patch(Rectangle((0.3, 6.30), 9.4, 0.95, fc=NAVY, ec="none"))
        ax.text(5.0, 6.77, "1.  Diagnose the damage type", fontsize=17, color=WHITE,
                ha="center", va="center", fontweight="bold")
        ax.annotate("", xy=(5.0, 5.92), xytext=(5.0, 6.25),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.0,
                                    mutation_scale=17))
        y = 4.90
        for dmg in ("Carbonate solids, scale", "Clay and silicate fines",
                    "Emulsion, organics, paraffin", "Deep or severe damage"):
            ax.add_patch(Rectangle((0.3, y), 9.4, 0.78, fc=WHITE, ec=BORDER, lw=1.4))
            ax.text(0.62, y + 0.39, dmg, fontsize=15, color=NAVY, va="center",
                    fontweight="bold")
            y -= 0.88
        ax.add_patch(Rectangle((0.3, 0.30), 9.4, 0.95, fc="#FDF2E4", ec=AMBER,
                               lw=2.0, ls=(0, (5, 3))))
        ax.text(5.0, 0.90, "2.  Verify with core flow tests before pumping", fontsize=15,
                color="#8C5A0E", ha="center", va="center", fontweight="bold")
        ax.text(5.0, 0.52, "wrong chemistry creates new damage", fontsize=15,
                color="#8C5A0E", ha="center", va="center", fontweight="bold")
    else:
        cols = [AMBER, TEAL, "#8E6BB0", RED]
        labels = ["HCl", "mud acid (HF/HCl)", "solvents, surfactants",
                  "hydraulic fracturing"]
        y = 4.90
        for col, lab in zip(cols, labels):
            ax.add_patch(Rectangle((0.3, y), 0.14, 0.78, fc=col, ec="none"))
            ax.annotate("", xy=(4.95, y + 0.39), xytext=(5.65, y + 0.39),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8,
                                        mutation_scale=15))
            ax.text(9.45, y + 0.39, lab, fontsize=15, color=col, va="center",
                    ha="right", fontweight="bold")
            y -= 0.88
    save(fig, "s19_tree_branches.png" if with_branches else "s19_tree_base.png",
         transparent=with_branches)


def fig_s19():
    _s19(False)
    _s19(True)


# ================================================================ S20  payback
def fig_s20():
    fig = plt.figure(figsize=(7.0, 3.6))
    ax = fig.add_axes([0.135, 0.195, 0.80, 0.765])
    t = np.linspace(0, 30, 200)
    ax.plot(t, 21075 * t, color=TEAL, lw=4.0, zorder=4)
    ax.axhline(300000, color=RED, lw=2.6, ls=(0, (6, 3)), zorder=3)
    ax.text(29.3, 318000, "job cost  $300,000", fontsize=16, color=RED, ha="right",
            va="bottom", fontweight="bold")
    ax.plot([14.2], [300000], "o", ms=12, mfc=WHITE, mec=NAVY, mew=3.0, zorder=6)
    ax.annotate("payback\n≈ 14 days", xy=(14.2, 300000), xytext=(16.6, 120000),
                fontsize=17, color=NAVY, fontweight="bold", linespacing=1.25,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6))
    ax.text(1.0, 520000, "cumulative net gain", fontsize=16, color=TEAL,
            fontweight="bold")
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 700000)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_yticks([0, 200000, 400000, 600000])
    ax.set_yticklabels(["0", "200k", "400k", "600k"])
    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Cumulative net gain ($)")
    clean(ax, grid="both")
    save(fig, "s20_econ.png")


# ================================================================ B4  drawdown
def fig_b4():
    fig = plt.figure(figsize=(6.0, 4.5))
    ax = fig.add_axes([0.145, 0.185, 0.70, 0.775])
    dd = np.array([200, 1500])
    ax.plot(dd, J0 * dd, color=TEAL, lw=3.8, label="Undamaged (S = 0)")
    ax.plot(dd, JD * dd, color=RED, lw=3.8, ls=(0, (6, 3.5)),
            label="Damaged (S = 8.55)")
    ax.set_xlim(0, 1600)
    ax.set_ylim(0, 7000)
    ax.set_xticks([200, 600, 1000, 1400])
    ax.set_yticks([0, 2000, 4000, 6000])
    thousands(ax, "y")
    ax.set_xlabel("Drawdown (psi)")
    ax.set_ylabel("Oil rate, q (STB/d)")
    clean(ax, grid="both")
    ax.legend(loc="upper left", fontsize=15)
    ax2 = ax.twinx()
    ax2.plot(dd, [FE_DAM, FE_DAM], color=NAVY, lw=2.6, ls=(0, (2, 3)))
    ax2.set_ylim(0, 1.0)
    ax2.set_ylabel("Flow efficiency (–)", color=NAVY, fontsize=15)
    ax2.tick_params(axis="y", colors=NAVY, labelsize=15)
    ax2.spines["top"].set_visible(False)
    ax2.text(1420, FE_DAM + 0.06, "FE = 0.447\n(flat)", color=NAVY, fontsize=15,
             fontweight="bold", ha="right", linespacing=1.25)
    save(fig, "b4_drawdown.png")


# ================================================================ icons (transparent)
def icon(fn, draw):
    fig = plt.figure(figsize=(0.85, 0.85))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    draw(ax)
    save(fig, fn, transparent=True)


def icons():
    def magnifier(ax):
        ax.add_patch(Circle((0.42, 0.60), 0.24, fc="none", ec=TEAL, lw=4.5))
        ax.plot([0.60, 0.84], [0.42, 0.18], color=TEAL, lw=6.0,
                solid_capstyle="round")

    def calculator(ax):
        ax.add_patch(FancyBboxPatch((0.20, 0.14), 0.60, 0.72,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc="none", ec=TEAL, lw=4.5))
        ax.plot([0.30, 0.70], [0.72, 0.72], color=TEAL, lw=4.0)
        for gx in (0.34, 0.50, 0.66):
            for gy in (0.32, 0.48):
                ax.add_patch(Circle((gx, gy), 0.045, fc=TEAL, ec="none"))

    def shield(ax):
        ax.add_patch(Polygon([[0.5, 0.90], [0.84, 0.74], [0.84, 0.44], [0.5, 0.12],
                              [0.16, 0.44], [0.16, 0.74]], closed=True, fc="none",
                             ec=TEAL, lw=4.5, joinstyle="round"))
        ax.plot([0.36, 0.46, 0.66], [0.52, 0.40, 0.66], color=TEAL, lw=4.5,
                solid_capstyle="round")

    icon("icon_magnifier.png", magnifier)
    icon("icon_calc.png", calculator)
    icon("icon_shield.png", shield)


if __name__ == "__main__":
    print("figures:")
    for f in (fig_s2, fig_s5, fig_s6, fig_s9, fig_s10, fig_s12, fig_s13, fig_s14,
              fig_s15, fig_s16, fig_s17, fig_s18, fig_s19, fig_s20, fig_b4, icons):
        f()
    print("done")
