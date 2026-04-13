#!/usr/bin/env python3
"""
Generate PNG diagram images for the Philosophy of Money slides.
Run from any directory; images are saved to PhilosophyOfMoney/visuals/.
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, 'visuals')
os.makedirs(OUT, exist_ok=True)

# ── Palette (matches money-philosophy.css) ────────────────────────────
BG      = '#0a0f1a'
GOLD    = '#c9a84c'
PARCH   = '#e8dcc8'
SLATE   = '#1a2535'
VERD    = '#5a8a7a'
COPPER  = '#b87333'
RED     = '#c0392b'
DIMGRAY = '#8a8578'

# ── Helpers ───────────────────────────────────────────────────────────

def new_fig(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis('off')
    return fig, ax


def box(ax, cx, cy, w, h, text, fc=SLATE, ec=GOLD, tc=PARCH, fs=9, bold=False):
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle='round,pad=0.05',
        facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=2, clip_on=False,
    )
    ax.add_patch(patch)
    ax.text(cx, cy, text, ha='center', va='center', color=tc,
            fontsize=fs, fontweight='bold' if bold else 'normal',
            multialignment='center', zorder=3)


def arrow(ax, x1, y1, x2, y2, c=GOLD):
    ax.annotate(
        '', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='->', color=c, lw=1.8, mutation_scale=14),
        zorder=4,
    )


def save(fig, fname):
    path = os.path.join(OUT, fname)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor=BG)
    plt.close(fig)
    print(f'  saved: {fname}')


# ═══════════════════════════════════════════════════════════════════════
# 1.  Virtuous vs Vicious Firm  (slide 4.3)
# ═══════════════════════════════════════════════════════════════════════
print('1. Virtuous vs Vicious Firm')
fig, ax = new_fig(11, 5.5)
ax.text(5.5, 5.15, 'Intellectual Virtues vs Vices in Organizations',
        ha='center', color=GOLD, fontsize=12, fontweight='bold')

box(ax, 2.75, 4.45, 4.0, 0.55, 'VIRTUOUS FIRM',
    fc='#162a1e', ec=VERD, tc=VERD, fs=10, bold=True)
box(ax, 8.25, 4.45, 4.0, 0.55, 'VICIOUS FIRM',
    fc='#2a1616', ec=COPPER, tc=COPPER, fs=10, bold=True)

rows_v = ['Encourages dissent', 'Stress-tests assumptions',
          'Admits mistakes quickly', 'Learns and adapts']
rows_x = ['Punishes doubt', 'Rewards groupthink',
          'Hides bad news', 'Repeats preventable failures']
ys = [3.55, 2.7, 1.85, 1.0]
bw, bh = 4.0, 0.62

for vt, xt, y in zip(rows_v, rows_x, ys):
    box(ax, 2.75, y, bw, bh, vt, fc='#162a1e', ec=VERD,   tc=PARCH, fs=9)
    box(ax, 8.25, y, bw, bh, xt, fc='#2a1616', ec=COPPER, tc=PARCH, fs=9)

for i in range(len(ys) - 1):
    arrow(ax, 2.75, ys[i] - bh / 2, 2.75, ys[i + 1] + bh / 2, c=VERD)
    arrow(ax, 8.25, ys[i] - bh / 2, 8.25, ys[i + 1] + bh / 2, c=COPPER)

ax.plot([5.5, 5.5], [0.6, 4.8], color='#2a3040', lw=1.2, ls='--', zorder=1)
save(fig, '4-3-virtuous-vs-vicious.png')


# ═══════════════════════════════════════════════════════════════════════
# 2.  LTCM Leverage Structure  (slide 4.4)
# ═══════════════════════════════════════════════════════════════════════
print('2. LTCM Leverage')
fig, ax = new_fig(7, 9)
ax.text(3.5, 8.65, 'LTCM: How Leverage Amplified Risk (1998)',
        ha='center', color=GOLD, fontsize=11, fontweight='bold')

steps = [
    ('Equity capital:  ~$4.7 billion',       SLATE,     GOLD),
    ('Leverage ratio:  ~25 to 1',            '#1c2c3e', GOLD),
    ('Total positions: ~$125 billion',       SLATE,     GOLD),
    ('Derivatives exposure: ~$1 trillion',   '#1c2c3e', GOLD),
    ('Small spread shock  (Russia default)', '#2c200e', COPPER),
    ('Margin calls + forced liquidation',    '#341808', COPPER),
    ('Fed-coordinated private rescue',       '#162a1e', VERD),
]
ys = np.linspace(7.8, 0.7, len(steps))
bh = 0.75
for (text, fc, ec), y in zip(steps, ys):
    box(ax, 3.5, y, 5.8, bh, text, fc=fc, ec=ec, fs=9.5)
for i in range(len(ys) - 1):
    arrow(ax, 3.5, ys[i] - bh / 2, 3.5, ys[i + 1] + bh / 2)
save(fig, '4-4-ltcm-leverage.png')


# ═══════════════════════════════════════════════════════════════════════
# 3.  2008 Model Failure Chain  (slide 5.3)
# ═══════════════════════════════════════════════════════════════════════
print('3. Model failure chain')
fig, ax = new_fig(14, 3.2)
ax.text(7, 2.95, '2008: From Model Assumption to Systemic Crisis',
        ha='center', color=GOLD, fontsize=11, fontweight='bold')

steps = [
    ('Model\nassumption',        SLATE,     GOLD),
    ('Risk output\n(AAA rated)', SLATE,     GOLD),
    ('Product\ndesign',          SLATE,     GOLD),
    ('High\nleverage',           '#241c0e', COPPER),
    ('Systemwide\nexposure',     '#2c1808', COPPER),
    ('Assumption\nfails',        '#361408', '#c05000'),
    ('Systemic\ncrisis',         '#3a0a0a', RED),
]
xs = np.linspace(1.1, 12.9, len(steps))
bw = 1.6
for (text, fc, ec), x in zip(steps, xs):
    box(ax, x, 1.5, bw, 0.9, text, fc=fc, ec=ec, fs=8.5)
for i in range(len(xs) - 1):
    arrow(ax, xs[i] + bw / 2, 1.5, xs[i + 1] - bw / 2, 1.5)
save(fig, '5-3-model-failure-chain.png')


# ═══════════════════════════════════════════════════════════════════════
# 4.  Interest Rate Spectrum  (slide 7.3)
# ═══════════════════════════════════════════════════════════════════════
print('4. Interest rate spectrum')
fig, ax = new_fig(12, 3.5)
ax.text(6, 3.25, 'Interest Rate Spectrum: Mortgages to Loan Sharks',
        ha='center', color=GOLD, fontsize=11, fontweight='bold')

items = [
    ('Mortgage\n~6% APR',       '#16281e', VERD,    PARCH),
    ('Car loan\n~8% APR',       '#1a2c1e', VERD,    PARCH),
    ('Credit card\n~25% APR',   '#2c2010', COPPER,  PARCH),
    ('Payday loan\n~400% APR',  '#341408', '#c05000', PARCH),
    ('Loan shark\nextreme APR', '#3a0808', RED,      PARCH),
]
xs  = np.linspace(1.4, 10.6, len(items))
bw, bh = 1.9, 0.9
for (text, fc, ec, tc), x in zip(items, xs):
    box(ax, x, 2.0, bw, bh, text, fc=fc, ec=ec, tc=tc, fs=9)
for i in range(len(xs) - 1):
    arrow(ax, xs[i] + bw / 2, 2.0, xs[i + 1] - bw / 2, 2.0)

ax.text(1.4,  0.8, 'lower ethical concern', color=VERD, fontsize=8, ha='left')
ax.text(10.6, 0.8, 'higher ethical concern', color=RED,  fontsize=8, ha='right')
ax.annotate('', xy=(10.3, 0.75), xytext=(1.7, 0.75),
            arrowprops=dict(arrowstyle='->', color=DIMGRAY, lw=1))
save(fig, '7-3-interest-spectrum.png')


# ═══════════════════════════════════════════════════════════════════════
# 5.  Legal to Fraud Spectrum  (slide 8.2)
# ═══════════════════════════════════════════════════════════════════════
print('5. Fraud spectrum')
fig, ax = new_fig(12, 3.8)
ax.text(6, 3.55, 'The Spectrum from Aggressive but Legal to Clear Fraud',
        ha='center', color=GOLD, fontsize=11, fontweight='bold')

items = [
    ('Aggressive\nbut legal',        '#1a2535', GOLD),
    ('Misleading\nomission',         '#251e14', COPPER),
    ('Reckless\nmisrepresentation',  '#2e1a0a', COPPER),
    ('Intentional\ndeception',       '#361208', '#c05000'),
    ('Clear\nfraud',                 '#3a0808', RED),
]
examples = [
    'High fees\ndisclosed',
    'Complex product,\nunsophisticated buyer',
    'Known flaws\nnot disclosed',
    'Sell while\nsecretly shorting',
    'Fabricated\ncollateral',
]
xs  = np.linspace(1.4, 10.6, len(items))
bw, bh = 1.9, 0.85
for (text, fc, ec), x in zip(items, xs):
    box(ax, x, 2.5, bw, bh, text, fc=fc, ec=ec, fs=9)
for ex, x in zip(examples, xs):
    ax.text(x, 1.6, ex, ha='center', va='center', color=DIMGRAY,
            fontsize=7.5, multialignment='center')
for i in range(len(xs) - 1):
    arrow(ax, xs[i] + bw / 2, 2.5, xs[i + 1] - bw / 2, 2.5)

ax.text(1.4,  0.7, 'legal',    color=GOLD, fontsize=8, ha='center')
ax.text(10.6, 0.7, 'criminal', color=RED,  fontsize=8, ha='center')
ax.annotate('', xy=(10.2, 0.65), xytext=(1.8, 0.65),
            arrowprops=dict(arrowstyle='->', color=DIMGRAY, lw=1))
save(fig, '8-2-fraud-spectrum.png')


# ═══════════════════════════════════════════════════════════════════════
# 6.  Public Banking Options  (slide 11.2)
# ═══════════════════════════════════════════════════════════════════════
print('6. Public banking options')
fig, ax = new_fig(10, 5.8)
ax.text(5, 5.5, 'Public Banking Pathways for the Unbanked',
        ha='center', color=GOLD, fontsize=11, fontweight='bold')

box(ax, 5, 4.6, 4.8, 0.75, 'Unbanked & Underbanked\nHouseholds', fs=10, bold=True)

mids = [
    (1.6, 3.0, 'Predatory options\n(payday, check-cashing)', '#2a1616', COPPER),
    (5.0, 3.0, 'Postal banking\n(low-fee public accounts)',  '#162a1e', VERD),
    (8.4, 3.0, 'Public bank\npartnerships',                  SLATE,     GOLD),
]
for cx, cy, text, fc, ec in mids:
    box(ax, cx, cy, 2.8, 0.82, text, fc=fc, ec=ec, fs=9)
    arrow(ax, 5, 4.6 - 0.375, cx, cy + 0.41)

leaves = [
    (5.0, 1.45, 'Nationwide\nbranch access',         '#162a1e', VERD),
    (8.4, 1.45, 'Local credit &\ndevelopment support', SLATE,   GOLD),
]
for cx, cy, text, fc, ec in leaves:
    box(ax, cx, cy, 2.8, 0.75, text, fc=fc, ec=ec, fs=9)
    arrow(ax, cx, 3.0 - 0.41, cx, cy + 0.375)

save(fig, '11-2-public-banking.png')

print(f'\nAll 6 diagrams written to {OUT}')
