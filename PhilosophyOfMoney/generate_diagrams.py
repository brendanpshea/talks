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
fig, ax = new_fig(14, 5.5)
ax.text(7, 5.2, '2008: From Model Assumption to Systemic Crisis',
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
    box(ax, x, 3.0, bw, 1.4, text, fc=fc, ec=ec, fs=9.5)
for i in range(len(xs) - 1):
    arrow(ax, xs[i] + bw / 2, 3.0, xs[i + 1] - bw / 2, 3.0)
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


# ═══════════════════════════════════════════════════════════════════════
# 7.  Rational Actor Model  (section 5, early slide)
# ═══════════════════════════════════════════════════════════════════════
print('7. Rational actor model')
fig, ax = new_fig(12, 4.8)
ax.text(6, 4.45, 'Rational Actor Model: Decision Flow',
        ha='center', color=GOLD, fontsize=12, fontweight='bold')

box(ax, 2.1, 2.6, 3.0, 1.35,
    'Inputs\nStable preferences\nFull information',
    fc=SLATE, ec=GOLD, fs=9.2)
box(ax, 6.0, 2.6, 3.2, 1.35,
    'Process\nCompare options\nExpected utility',
    fc='#1c2c3e', ec=GOLD, fs=9.2)
box(ax, 9.9, 2.6, 3.0, 1.35,
    'Choice\nSelect utility-\nmaximizing action',
    fc='#162a1e', ec=VERD, fs=9.2)

arrow(ax, 3.6, 2.6, 4.4, 2.6)
arrow(ax, 7.6, 2.6, 8.4, 2.6)

ax.text(6, 0.85,
        'Market claim: aggregating many such choices yields informative prices',
        ha='center', color=DIMGRAY, fontsize=9)

save(fig, '5-2-rational-actor-model.png')


# ═══════════════════════════════════════════════════════════════════════
# 8.  Insider Trading Decision Tree  (slide 8.3)
# ═══════════════════════════════════════════════════════════════════════
print('8. Insider trading decision tree')
fig, ax = new_fig(12, 5.6)
ax.text(6, 5.25, 'Insider Trading: A Rough Decision Tree',
        ha='center', color=GOLD, fontsize=12, fontweight='bold')

box(ax, 6.0, 4.45, 4.6, 0.9, 'Do you have nonpublic, material information?',
    fc=SLATE, ec=GOLD, fs=9.5, bold=True)
box(ax, 3.3, 3.15, 4.0, 0.85, 'NO\nLikely legal research/trading',
    fc='#162a1e', ec=VERD, fs=9)
box(ax, 8.7, 3.15, 4.0, 0.85, 'YES\nHow was it obtained?',
    fc='#2c200e', ec=COPPER, fs=9)

box(ax, 6.3, 1.8, 3.6, 0.85, 'Duty breached\nor tipped source?',
    fc='#341808', ec='#c05000', fs=9)
box(ax, 10.4, 1.8, 3.0, 0.85, 'Public/independent\nchannel?',
    fc='#1c2c3e', ec=GOLD, fs=9)

box(ax, 5.1, 0.6, 2.6, 0.75, 'High legal risk\nof insider trading',
    fc='#3a0808', ec=RED, fs=8.8)
box(ax, 8.0, 0.6, 2.6, 0.75, 'Gray zone\nneeds facts',
    fc='#2e1a0a', ec=COPPER, fs=8.8)
box(ax, 10.9, 0.6, 2.0, 0.75, 'Usually\npermitted',
    fc='#162a1e', ec=VERD, fs=8.8)

arrow(ax, 6.0, 4.0, 3.8, 3.58)
arrow(ax, 6.0, 4.0, 8.2, 3.58)
arrow(ax, 8.7, 2.72, 6.7, 2.22)
arrow(ax, 8.7, 2.72, 10.1, 2.22)
arrow(ax, 6.3, 1.36, 5.4, 0.97)
arrow(ax, 6.3, 1.36, 7.7, 0.97)
arrow(ax, 10.4, 1.36, 10.8, 0.97)

ax.text(6, 0.12, 'Educational simplification, not legal advice',
        ha='center', color=DIMGRAY, fontsize=8)
save(fig, '8-3-insider-trading-tree.png')


# ═══════════════════════════════════════════════════════════════════════
# 9.  How Crypto Works (roughly)  (new slide in section 10)
# ═══════════════════════════════════════════════════════════════════════
print('9. Crypto workflow')
fig, ax = new_fig(13, 4.6)
ax.text(6.5, 4.25, 'How Crypto Works (Roughly)',
        ha='center', color=GOLD, fontsize=12, fontweight='bold')

steps = [
    ('Wallet signs\ntransaction', '#1c2c3e', GOLD),
    ('Broadcast to\npeer network', SLATE, GOLD),
    ('Mempool holds\npending tx', '#1c2c3e', GOLD),
    ('Miners/validators\norder + verify', '#2c200e', COPPER),
    ('Block appended\nto chain', '#162a1e', VERD),
]
xs = np.linspace(1.6, 11.4, len(steps))
for (text, fc, ec), x in zip(steps, xs):
    box(ax, x, 2.35, 2.25, 1.15, text, fc=fc, ec=ec, fs=9)
for i in range(len(xs) - 1):
    arrow(ax, xs[i] + 1.12, 2.35, xs[i + 1] - 1.12, 2.35)

ax.text(6.5, 0.75, 'Security comes from cryptography + distributed consensus, not from a central bank.',
        ha='center', color=DIMGRAY, fontsize=9)
save(fig, '10-1-crypto-how-it-works.png')


# ═══════════════════════════════════════════════════════════════════════
# 10. Crypto Practical Record Timeline  (slide 10.2)
# ═══════════════════════════════════════════════════════════════════════
print('10. Crypto practical record timeline')
fig, ax = new_fig(12.5, 4.8)
ax.text(6.25, 4.45, 'Crypto in Practice: Mixed Record',
        ha='center', color=GOLD, fontsize=12, fontweight='bold')

events = [
    ('Volatility', 'Large price swings\nlimit daily use', '#2e1a0a', COPPER),
    ('Fraud/Collapse', 'FTX and similar\nplatform failures', '#3a0808', RED),
    ('Energy Costs', 'Proof-of-work can\nbe resource intensive', '#2c200e', COPPER),
    ('Useful Niches', 'Capital controls,\nremittances, instability', '#162a1e', VERD),
]
xs = [1.8, 4.5, 7.2, 9.9]
for (title, desc, fc, ec), x in zip(events, xs):
    box(ax, x, 2.5, 2.3, 1.45, f'{title}\n{desc}', fc=fc, ec=ec, fs=8.8)
for i in range(len(xs) - 1):
    arrow(ax, xs[i] + 1.15, 2.5, xs[i + 1] - 1.15, 2.5)

ax.text(6.25, 0.7, 'Bottom line: meaningful innovation, but weak consumer protection and unstable value.',
        ha='center', color=DIMGRAY, fontsize=9)
save(fig, '10-2-crypto-practical-record.png')


# ═══════════════════════════════════════════════════════════════════════
# 11. Public Money Concept Map  (new slide in section 11)
# ═══════════════════════════════════════════════════════════════════════
print('11. Public money concept map')
fig, ax = new_fig(12, 5.2)
ax.text(6, 4.9, 'What Is Public Money?',
        ha='center', color=GOLD, fontsize=12, fontweight='bold')

box(ax, 6, 3.9, 4.2, 0.9, 'Public Money\nLiabilities of the state/central bank',
    fc='#1c2c3e', ec=GOLD, fs=9.5, bold=True)
box(ax, 2.2, 2.3, 3.2, 0.9, 'Issued by\npublic authority', fc=SLATE, ec=GOLD, fs=9)
box(ax, 6.0, 2.3, 3.2, 0.9, 'Accepted for\ntaxes and fees', fc='#162a1e', ec=VERD, fs=9)
box(ax, 9.8, 2.3, 3.2, 0.9, 'Backed by legal\nand policy power', fc='#2c200e', ec=COPPER, fs=9)

box(ax, 3.1, 0.8, 2.6, 0.8, 'Cash', fc='#162a1e', ec=VERD, fs=9)
box(ax, 6.0, 0.8, 2.6, 0.8, 'Bank reserves', fc=SLATE, ec=GOLD, fs=9)
box(ax, 8.9, 0.8, 2.6, 0.8, 'Potential CBDC', fc='#1c2c3e', ec=GOLD, fs=9)

for x in [2.2, 6.0, 9.8]:
    arrow(ax, 6.0, 3.45, x, 2.75)
for x1, x2 in [(2.2, 3.1), (6.0, 6.0), (9.8, 8.9)]:
    arrow(ax, x1, 1.85, x2, 1.2)

save(fig, '11-1-public-money-map.png')


# ═══════════════════════════════════════════════════════════════════════
# 12. Cash vs Crypto vs CBDC Matrix  (slide 11.3)
# ═══════════════════════════════════════════════════════════════════════
print('12. Cash crypto cbdc matrix')
fig, ax = new_fig(12.5, 6.0)
ax.text(6.25, 5.65, 'Cash vs Crypto vs CBDC: Tradeoff Matrix',
        ha='center', color=GOLD, fontsize=12, fontweight='bold')

cols = [('Cash', '#162a1e', VERD), ('Crypto', '#2c200e', COPPER), ('CBDC', '#1c2c3e', GOLD)]
rows = [
    ('Privacy', 'High in person', 'Pseudonymous', 'Policy-dependent'),
    ('Stability', 'High nominal', 'Often low', 'High nominal'),
    ('Access', 'Offline capable', 'Needs internet', 'Could be universal'),
    ('Control', 'State bearer form', 'Protocol/platform', 'Central governance'),
    ('Resilience', 'Works offline', 'Custody/network risk', 'Infra dependent'),
]

ax.text(1.3, 4.95, 'Dimension', color=GOLD, fontsize=9.5, ha='left', fontweight='bold')
for i, (name, _, ec) in enumerate(cols):
    ax.text(4.1 + i * 2.75, 4.95, name, color=ec, fontsize=9.5, ha='center', fontweight='bold')

y = 4.2
for rname, c1, c2, c3 in rows:
    box(ax, 1.35, y, 2.2, 0.72, rname, fc=SLATE, ec=GOLD, fs=8.7, bold=True)
    box(ax, 4.1, y, 2.35, 0.72, c1, fc='#162a1e', ec=VERD, fs=8.1)
    box(ax, 6.85, y, 2.35, 0.72, c2, fc='#2c200e', ec=COPPER, fs=8.1)
    box(ax, 9.6, y, 2.35, 0.72, c3, fc='#1c2c3e', ec=GOLD, fs=8.1)
    y -= 0.9

save(fig, '11-3-cash-crypto-cbdc-matrix.png')

print(f'\nAll 12 diagrams written to {OUT}')
