#!/usr/bin/env python3
"""
生成静态截图展示点击效果
"""

import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import os

# 数据文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_file = os.path.join(parent_dir, 'data', 'typhoon_mangkhut.html')

print(f"正在生成静态截图展示...")

# 数据解析
with open(data_file, 'r', encoding='utf-8') as f:
    html = f.read()
soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', class_='data_table')
rows = table.find_all('tr')[2:]
data = []
for row in rows:
    cols = [td.get_text(strip=True) for td in row.find_all('td')]
    if len(cols) == 9:
        data.append({
            '站点': cols[0],
            '最高阵风风向': cols[1],
            '最高阵风风速': cols[2],
            '最高阵风日期': cols[3],
            '最高阵风时间': cols[4]
        })

df = pd.DataFrame(data)
df['最高阵风风速'] = pd.to_numeric(df['最高阵风风速'], errors='coerce').fillna(0)
df = df[df['最高阵风风速'] > 0].reset_index(drop=True)

stations = df['站点'].values
speeds = df['最高阵风风速'].values
wind_dirs = df['最高阵风风向'].values

# 视觉设置
N = len(stations)
angles = np.linspace(0, 2*np.pi, N, endpoint=False)
radii = np.log1p(speeds) * 20

x = radii * np.cos(angles)
y = radii * np.sin(angles)

colors = plt.cm.viridis(speeds / speeds.max())
sizes = speeds * 5 + 50

# 创建截图1：基础视图 - 使用与原始程序完全相同的设置
fig1, ax1 = plt.subplots(figsize=(10, 10))
fig1.patch.set_facecolor("black")
ax1.set_facecolor("black")
ax1.axis("off")

# 添加标题 - 与原始程序完全一致
fig1.suptitle('TYPHOON MANGKHUT - WIND SPEED VISUALIZATION', 
             fontsize=18, 
             fontweight='bold', 
             color='white', 
             y=0.95,
             fontfamily='monospace')

# 添加操作提示 - 这是缺少的第二行文字！
ax1.text(0.5, 0.88, 'Click on any station dot for detailed information', 
        transform=fig1.transFigure, 
        fontsize=10, 
        color='lightgray', 
        ha='center',
        fontfamily='monospace',
        alpha=0.8,
        style='italic')

# 添加副标题
ax1.text(0.5, 0.02, 'Hong Kong Weather Stations | September 2018', 
        transform=ax1.transAxes, 
        fontsize=12, 
        color='cyan', 
        ha='center',
        fontfamily='monospace',
        alpha=0.8)

max_radius = np.max(radii) * 1.4
ax1.set_xlim(-max_radius, max_radius)
ax1.set_ylim(-max_radius, max_radius)

scat1 = ax1.scatter(x, y, s=sizes, c=colors, alpha=0.8, edgecolors="white", linewidth=0.5)

# 保存基础视图
fig1.savefig(os.path.join(parent_dir, 'assets', 'screenshot_basic.png'), 
            dpi=150, facecolor='black', bbox_inches='tight')
print("✓ 生成基础视图截图: assets/screenshot_basic.png")

# 创建截图2：点击效果展示 - 使用与原始程序相同的设置
fig2, ax2 = plt.subplots(figsize=(10, 10))
fig2.patch.set_facecolor("black")
ax2.set_facecolor("black")
ax2.axis("off")

# 添加标题
fig2.suptitle('TYPHOON MANGKHUT - WIND SPEED VISUALIZATION', 
             fontsize=18, 
             fontweight='bold', 
             color='white', 
             y=0.95,
             fontfamily='monospace')

# 添加操作提示
ax2.text(0.5, 0.88, 'Example: Clicking on Cheung Chau Station shows details', 
        transform=fig2.transFigure, 
        fontsize=10, 
        color='lightgray', 
        ha='center',
        fontfamily='monospace',
        alpha=0.8,
        style='italic')

# 添加副标题
ax2.text(0.5, 0.02, 'Hong Kong Weather Stations | September 2018', 
        transform=ax2.transAxes, 
        fontsize=12, 
        color='cyan', 
        ha='center',
        fontfamily='monospace',
        alpha=0.8)

ax2.set_xlim(-max_radius, max_radius)
ax2.set_ylim(-max_radius, max_radius)

# 高亮某个点（长洲）
highlight_idx = 2
highlighted_sizes = sizes.copy()
highlighted_sizes[highlight_idx] *= 2

scat2 = ax2.scatter(x, y, s=highlighted_sizes, c=colors, alpha=0.8, edgecolors="white", linewidth=0.5)

# 添加水波纹效果
for i in range(3):
    radius = 30 + i * 20
    alpha = 0.8 - i * 0.2
    circle = plt.Circle((x[highlight_idx], y[highlight_idx]), radius, fill=False, 
                       color='cyan', alpha=alpha, linewidth=2)
    ax2.add_patch(circle)

# 添加信息框 - 使用与原始程序完全相同的样式和定位
info_text = f"STATION: Cheung Chau\nWIND SPEED: {int(speeds[highlight_idx])} km/h\nDIRECTION: E\nTIME: 16/9 14:10"

# 使用annotate来创建信息框，与原始程序保持一致
annotation = ax2.annotate(
    info_text,
    xy=(0, 0), xytext=(0.5, 0.5),
    textcoords="axes fraction",
    bbox=dict(boxstyle="round,pad=1.0", fc="black", alpha=0.8, edgecolor="cyan", linewidth=2),
    fontsize=14,
    color="white",
    ha="center",
    va="center",
    fontfamily="monospace"
)
annotation.set_visible(True)

# 保存点击效果截图
fig2.savefig(os.path.join(parent_dir, 'assets', 'screenshot_clicked.png'), 
            dpi=150, facecolor='black', bbox_inches='tight')
print("✓ 生成点击效果截图: assets/screenshot_clicked.png")

plt.close('all')
print("\n静态截图生成完成！现在可以配合GIF使用来完整展示交互功能。")