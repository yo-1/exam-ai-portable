# -*- coding: utf-8 -*-
"""図表サンプル生成: 棒・折れ線・円グラフ (GIS/測量テーマの仮データ)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, os

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Yu Gothic", "Meiryo", "Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
rng = np.random.RandomState(42)

# 棒グラフ: 地区別の森林率
districts = ["北部", "中央", "東部", "西部", "南部"]
forest = [68.4, 45.2, 57.9, 39.6, 52.3]
fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=200)
bars = ax.bar(districts, forest, color="#4a7fb5", edgecolor="#2c4f73")
for b, v in zip(bars, forest):
    ax.text(b.get_x() + b.get_width()/2, v + 1.2, f"{v:.1f}%", ha="center", fontsize=10)
ax.set_ylabel("森林率（%）"); ax.set_ylim(0, 80)
ax.set_title("地区別 森林率（サンプル）")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/chart_bar.png"); plt.close(fig)

# 折れ線: 年度別のドローン測量実施面積
years = np.arange(2019, 2026)
area = np.array([12, 25, 41, 68, 95, 128, 164])
fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=200)
ax.plot(years, area, marker="o", color="#d43d2a", lw=2)
ax.fill_between(years, area, alpha=0.12, color="#d43d2a")
ax.set_ylabel("測量実施面積（ha）"); ax.set_xticks(years)
ax.set_title("年度別 ドローン測量実施面積の推移（サンプル）")
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f"{OUT}/chart_line.png"); plt.close(fig)

# 円グラフ: 土地利用構成比
labels = ["森林", "農地", "宅地", "公共用地", "水域", "その他"]
vals = [46, 18, 15, 8, 5, 8]
colors = ["#5b8c5a", "#d9b44a", "#b5654a", "#7a7a7a", "#4a7fb5", "#c9c9c9"]
fig, ax = plt.subplots(figsize=(6.4, 4.6), dpi=200)
ax.pie(vals, labels=labels, colors=colors, autopct="%1.0f%%",
       pctdistance=0.75, textprops={"fontsize": 10},
       wedgeprops={"edgecolor": "white", "linewidth": 1.5})
ax.set_title("土地利用構成比（サンプル）")
fig.tight_layout(); fig.savefig(f"{OUT}/chart_pie.png"); plt.close(fig)
print("charts done:", sorted(os.listdir(OUT)))
