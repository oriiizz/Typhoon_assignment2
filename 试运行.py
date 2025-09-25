# -*- coding: utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.patches as mpatches

# 1. 解析本地HTML文件，提取气象站风力数据
html_file = 'typhoon_mangkhut.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', class_='data_table')
rows = table.find_all('tr')[2:]  # 跳过前两行表头
data = []
for row in rows:
    cols = [td.get_text(strip=True) for td in row.find_all('td')]
    if len(cols) == 9:
        data.append({
            '站点': cols[0],
            '最高阵风风向': cols[1],
            '最高阵风风速': cols[2],
            '最高阵风日期': cols[3],
            '最高阵风时间': cols[4],
            '最高平均风速风向': cols[5],
            '最高平均风速': cols[6],
            '最高平均风速日期': cols[7],
            '最高平均风速时间': cols[8]
        })

# 2. 创建DataFrame
df = pd.DataFrame(data)

# --------- 动画：风向-风速散点 ---------
df_anim = df.copy()
df_anim['最高阵风风速'] = pd.to_numeric(df_anim['最高阵风风速'], errors='coerce').fillna(0)
df_anim = df_anim[df_anim['最高阵风风速'] > 0].reset_index(drop=True)
stations = df_anim['站点'].values
speeds = df_anim['最高阵风风速'].values
wind_dirs = df_anim['最高阵风风向'].values
times = [f"{d} {t}" for d, t in zip(df_anim['最高阵风日期'], df_anim['最高阵风时间'])]

unique_dirs = list(df_anim['最高阵风风向'].unique())
dir_to_x = {d: i for i, d in enumerate(unique_dirs)}
x_vals = np.array([dir_to_x[d] for d in wind_dirs])
y_vals = speeds

order = np.arange(len(stations))
np.random.seed(42)
np.random.shuffle(order)

fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor('#f0f0f0')
ax.set_facecolor('#f8f8ff')
ax.set_xticks(range(len(unique_dirs)))
ax.set_xticklabels(unique_dirs, fontsize=11, rotation=30)
ax.set_xlabel('Wind Direction', fontsize=13)
ax.set_ylabel('Gust Speed (km/h)', fontsize=13)
ax.set_ylim(0, max(y_vals)*1.15)
ax.set_xlim(-0.5, len(unique_dirs)-0.5)
ax.set_title('Typhoon Mangkhut: Gust Speed by Station and Wind Direction', fontsize=15, fontweight='bold', y=1.03)

main_scatter = None
annotation = None
if hasattr(ax, 'ripple_patch'):
    ax.ripple_patch = None

def update(frame):
    global main_scatter
    if hasattr(update, 'ripple_patch') and update.ripple_patch:
        try:
            update.ripple_patch.remove()
        except Exception:
            pass
        update.ripple_patch = None
    if frame < len(order):
        hi_idx = order[frame]
    else:
        hi_idx = order[-1]
    dists = np.abs(y_vals - y_vals[hi_idx])
    if dists.max() > 0:
        norm_dists = dists / dists.max()
    else:
        norm_dists = np.zeros_like(dists)
    alphas = 1.0 - 0.85 * norm_dists
    alphas[hi_idx] = 1.0
    base_sizes = np.clip(y_vals * 2 + 40, 50, 300)
    grow_frames = 30
    grow = min(1.0, (frame % grow_frames) / (grow_frames - 1)) if frame < len(order) else 1.0
    sizes = base_sizes.copy()
    sizes[hi_idx] = base_sizes[hi_idx] * (1.0 + 1.2 * grow)
    if main_scatter:
        main_scatter.remove()
    main_scatter = ax.scatter(
        x_vals, y_vals,
        s=sizes,
        c='#1f77b4',
        alpha=alphas,
        edgecolors='white',
        linewidth=2,
        zorder=2,
        picker=True,
        pickradius=10
    )
    if frame < len(order):
        ripple_max_pix = 120
        ripple_pix = 30 + (ripple_max_pix - 30) * grow
        x0, y0 = x_vals[hi_idx], y_vals[hi_idx]
        trans = ax.transData
        x0_disp, y0_disp = trans.transform((x0, y0))
        x1_disp, _ = trans.transform((x0 + 1, y0))
        data_per_pix = abs(x1_disp - x0_disp)
        if data_per_pix == 0:
            data_per_pix = 1
        ripple_radius_data = ripple_pix / data_per_pix
        update.ripple_patch = mpatches.Circle(
            (x0, y0),
            radius=ripple_radius_data,
            edgecolor='#1f77b4',
            facecolor='none',
            lw=2,
            alpha=0.5 * (1 - grow),
            zorder=1
        )
        ax.add_patch(update.ripple_patch)
        return [main_scatter, update.ripple_patch]
    else:
        update.ripple_patch = None
        return [main_scatter]

def on_pick(event):
    global annotation
    if annotation:
        annotation.remove()
        annotation = None
    ind = event.ind[0]
    station_name = stations[ind]
    wind_speed = y_vals[ind]
    wind_dir = wind_dirs[ind]
    time_str = times[ind]
    text = f"Station: {station_name}\\nGust: {wind_speed} km/h\\nDirection: {wind_dir}\\nTime: {time_str}"
    x, y = x_vals[ind], y_vals[ind]
    annotation = ax.annotate(
        text,
        xy=(x, y),
        xytext=(20, 20),
        textcoords="offset points",
        bbox=dict(
            boxstyle="round,pad=0.5",
            facecolor="lightyellow",
            alpha=0.9,
            edgecolor="#1f77b4",
            linewidth=2
        ),
        fontsize=10,
        fontweight='bold',
        arrowprops=dict(
            arrowstyle="->",
            connectionstyle="arc3,rad=0.3",
            color="#1f77b4"
        )
    )
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', on_pick)
info_text = ax.text(
    0.02, 0.98,
    'All stations shown. Highlighted station animates with ripple.\\nX: Wind direction (category), Y: Gust speed (km/h).',
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment='top',
    bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8)
)
ani = FuncAnimation(
    fig,
    update,
    frames=len(order) + 20,
    interval=1000,
    blit=False,
    repeat=False
)
plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.show()