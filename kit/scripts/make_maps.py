# -*- coding: utf-8 -*-
"""地理情報サンプル生成: コロプレス / 標高・陰影図 / 点分布ヒートマップ (すべて合成データ)"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, os
from scipy.spatial import Voronoi
from scipy.ndimage import gaussian_filter
from scipy.stats import gaussian_kde
from shapely.geometry import Polygon, box
import geopandas as gpd

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Yu Gothic", "Meiryo", "Noto Sans CJK JP", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
os.makedirs(OUT, exist_ok=True)
rng = np.random.RandomState(7)

def finite_voronoi(vor, radius):
    """無限領域を有限化する定石レシピ"""
    new_regions, new_vertices = [], vor.vertices.tolist()
    center = vor.points.mean(axis=0)
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))
    for p1, region in enumerate(vor.point_region):
        verts = vor.regions[region]
        if all(v >= 0 for v in verts):
            new_regions.append(verts); continue
        ridges = all_ridges[p1]
        new_region = [v for v in verts if v >= 0]
        for p2, v1, v2 in ridges:
            if v2 < 0: v1, v2 = v2, v1
            if v1 >= 0: continue
            t = vor.points[p2] - vor.points[p1]
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])
            mid = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(mid - center, n)) * n
            far = vor.vertices[v2] + direction * radius
            new_region.append(len(new_vertices)); new_vertices.append(far.tolist())
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        order = np.argsort(np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0]))
        new_regions.append([new_region[i] for i in order])
    return new_regions, np.asarray(new_vertices)

# ---- 1. コロプレスマップ ----
W, H = 100.0, 80.0
pts = rng.rand(30, 2) * [W, H]
vor = Voronoi(pts)
regions, vertices = finite_voronoi(vor, 200.0)
region_box = box(0, 0, W, H)
polys, vals = [], []
for reg in regions:
    p = Polygon(vertices[reg]).intersection(region_box)
    if p.is_empty or p.area < 20:
        continue
    cx = p.centroid.x
    vals.append(round(22 + 14 * (cx / W) + rng.rand() * 6, 1))
    polys.append(p)
gdf = gpd.GeoDataFrame({"aging_rate": vals}, geometry=polys, crs="EPSG:3857")
fig, ax = plt.subplots(figsize=(7.6, 6.0), dpi=200)
gdf.plot(column="aging_rate", cmap="YlOrRd", edgecolor="white", linewidth=0.8,
         legend=True, ax=ax, legend_kwds={"label": "高齢化率（%）", "shrink": 0.75})
ax.set_title("地区別 高齢化率の分布（サンプル表示）")
ax.set_xticks([]); ax.set_yticks([]); ax.set_xlabel(""); ax.set_ylabel("")
fig.tight_layout(); fig.savefig(f"{OUT}/map_choropleth.png"); plt.close(fig)
gdf.to_file(f"{OUT}/sample_polygons.gpkg", layer="districts", driver="GPKG")

# ---- 2. 標高・陰影図: ガウス平滑ノイズの重ね合わせで作る合成DEM ----
n = 400
dem = np.zeros((n, n))
for sigma, amp in [(55, 300), (24, 150), (10, 60), (4, 22)]:
    dem += amp * gaussian_filter(rng.rand(n, n), sigma)
ridge = np.exp(-((np.linspace(-1, 1, n)[None, :] - 0.25 * np.sin(np.linspace(0, 3, n))[:, None]) ** 2) / 0.02)
dem += 180 * ridge   # 尾根筋を1本通す
dem = (dem - dem.min()) / (dem.max() - dem.min()) * 820 + 40
dy, dx = np.gradient(dem, 25, 25)
slope = np.arctan(np.hypot(dx, dy)); aspect = np.arctan2(-dy, dx)
az, alt = np.deg2rad(315), np.deg2rad(45)
hs = np.sin(alt) * np.cos(slope) + np.cos(alt) * np.sin(slope) * np.cos(az - aspect)
hs = (hs - hs.min()) / (hs.max() - hs.min())
fig, ax = plt.subplots(figsize=(7.6, 6.4), dpi=200)
ax.imshow(hs, cmap="gray", vmin=0.25, vmax=1.0)
im = ax.imshow(dem, cmap="terrain", alpha=0.55, vmin=40, vmax=860)
cbar = fig.colorbar(im, ax=ax, shrink=0.85); cbar.set_label("標高（m）")
ax.set_title("標高段彩図＋陰影起伏図（サンプルDEM解析結果）")
ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(f"{OUT}/map_dem.png"); plt.close(fig)
np.save(f"{OUT}/sample_dem.npy", dem.astype(np.float32))

# ---- 3. 点分布 + ヒートマップ + バッファ ----
centers = np.array([[25, 55], [55, 30], [78, 62], [45, 72]])
px, py = [], []
for c in centers:
    k = rng.randint(90, 170)
    px.append(rng.normal(c[0], 6.5, k)); py.append(rng.normal(c[1], 5.5, k))
px = np.concatenate(px); py = np.concatenate(py)
keep = (px >= 0) & (px <= W) & (py >= 0) & (py <= H)
px, py = px[keep], py[keep]
gx, gy = np.mgrid[0:W:200j, 0:H:160j]
dens = gaussian_kde(np.vstack([px, py]))(np.vstack([gx.ravel(), gy.ravel()])).reshape(gx.shape)
fig, ax = plt.subplots(figsize=(7.6, 6.0), dpi=200)
ax.imshow(dens.T, origin="lower", extent=[0, W, 0, H], cmap="YlOrRd", alpha=0.85)
ax.scatter(px, py, s=3, c="#20303c", alpha=0.55, label="公共施設（仮）")
for c in centers[:2]:
    ax.add_patch(plt.Circle(c, 12, fill=False, edgecolor="#1f6fb2", lw=1.6, linestyle="--"))
ax.set_title("公共施設の分布と密度（サンプル解析：カーネル密度＋到達圏）")
ax.set_xticks([]); ax.set_yticks([]); ax.legend(loc="lower left", fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/map_points.png"); plt.close(fig)
print("maps redone")
