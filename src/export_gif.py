#!/usr/bin/env python3
"""
台风山竹数据可视化 - GIF导出版本
专门用于生成动画GIF文件
"""

import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import os

# 数据文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
data_file = os.path.join(parent_dir, 'data', 'typhoon_mangkhut.html')
output_file = os.path.join(parent_dir, 'assets', 'typhoon.gif')

print(f"正在读取数据文件: {data_file}")
print(f"GIF将保存到: {output_file}")

# 使用和主程序相同的数据解析逻辑
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
            '最高阵风时间': cols[4],
            '最高平均风速风向': cols[5],
            '最高平均风速': cols[6],
            '最高平均风速日期': cols[7],
            '最高平均风速时间': cols[8]
        })

df = pd.DataFrame(data)
df['最高阵风风速'] = pd.to_numeric(df['最高阵风风速'], errors='coerce').fillna(0)
df = df[df['最高阵风风速'] > 0].reset_index(drop=True)

stations = df['站点'].values
speeds = df['最高阵风风速'].values
wind_dirs = df['最高阵风风向'].values
times = [f"{d} {t}" for d, t in zip(df['最高阵风日期'], df['最高阵风时间'])]

print(f"成功读取 {len(df)} 个气象站数据")

# 使用和主程序相同的视觉设置
N = len(stations)
angles = np.linspace(0, 2*np.pi, N, endpoint=False)
radii = np.log1p(speeds) * 20

# 初始位置（极坐标转直角坐标）
x = radii * np.cos(angles)
y = radii * np.sin(angles)

colors = plt.cm.viridis(speeds / speeds.max())
sizes = speeds * 5 + 50
original_sizes = sizes.copy()

# 创建图形
fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.axis("off")

# 添加标题
fig.suptitle('TYPHOON MANGKHUT - WIND SPEED VISUALIZATION', 
             fontsize=18, 
             fontweight='bold', 
             color='white', 
             y=0.95,
             fontfamily='monospace')

# 添加副标题
ax.text(0.5, 0.02, 'Hong Kong Weather Stations | September 2018', 
        transform=ax.transAxes, 
        fontsize=12, 
        color='cyan', 
        ha='center',
        fontfamily='monospace',
        alpha=0.8)

# 设置显示范围
max_radius = np.max(radii) * 1.4
ax.set_xlim(-max_radius, max_radius)
ax.set_ylim(-max_radius, max_radius)

# 创建初始散点图
scat = ax.scatter(x, y, s=sizes, c=colors, alpha=0.8, edgecolors="white", linewidth=0.5)

# 动画变量
frame_count = 0

def update(frame):
    global frame_count
    
    frame_count = frame
    
    # 计算动画效果
    breathing = 1.0 + 0.1 * np.sin(frame * 0.15)
    rotation = frame * 0.01
    size_variation = 1.0 + 0.08 * np.sin(frame * 0.2 + np.arange(N) * 0.3)
    
    # 计算新位置
    new_angles = angles + rotation
    new_x = radii * np.cos(new_angles) * breathing
    new_y = radii * np.sin(new_angles) * breathing
    
    # 计算新大小
    new_sizes = original_sizes * size_variation
    
    # 更新散点图
    scat.set_offsets(np.column_stack([new_x, new_y]))
    scat.set_sizes(new_sizes)
    
    return [scat]

print("开始生成GIF动画...")
print("这可能需要几分钟时间，请耐心等待...")

# 创建动画并保存为GIF
ani = FuncAnimation(fig, update, frames=200, interval=80, blit=False)

# 导出GIF
ani.save(output_file, writer="pillow", fps=12, dpi=80)

print(f"GIF导出完成！")
print(f"文件位置: {output_file}")
print(f"文件大小: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")

plt.close()