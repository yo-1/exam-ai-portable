# -*- coding: utf-8 -*-
"""標高・陰影図のみ再生成 (合成DEM: 尾根+丘陵+平野のバランス調整版)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, os
from scipy.ndimage import gaussian_filter

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Yu Gothic", "Meiryo", "Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
rng = np.random.RandomState(11)
n = 400
dem = np.zeros((n, n))
for sigma, amp in [(55, 260), (24, 190), (10, 95), (4, 38)]:
    dem += amp * gaussian_filter(rng.rand(n, n), sigma)
xx = np.linspace(-1, 1, n)[None, :]
yy = np.linspace(0, 3, n)[:, None]
ridge = np.exp(-((xx - 0.3 * np.sin(yy)) ** 2) / 0.045)
dem += 150 * ridge                      # 尾根筋 (幅広め)
dem += 90 * np.clip(xx, 0, None)        # 東側へ緩く隆起
dem = (dem - dem.min()) / (dem.max() - dem.min()) * 820 + 40
dy, dx = np.gradient(dem, 25, 25)
slope = np.arctan(np.hypot(dx, dy)); aspect = np.arctan2(-dy, dx)
az, alt = np.deg2rad(315), np.deg2rad(45)
hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
hs = (hs - hs.min()) / (hs.max() - hs.min())
fig, ax = plt.subplots(figsize=(7.6, 6.4), dpi=200)
ax.imshow(hs, cmap="gray", vmin=0.2, vmax=1.0)
im = ax.imshow(dem, cmap="terrain", alpha=0.5, vmin=40, vmax=860)
cbar = fig.colorbar(im, ax=ax, shrink=0.85); cbar.set_label("標高（m）")
ax.set_title("標高段彩図＋陰影起伏図（サンプルDEM解析結果）")
ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(f"{OUT}/map_dem.png"); plt.close(fig)
np.save(f"{OUT}/sample_dem.npy", dem.astype(np.float32))
print("dem redone")
