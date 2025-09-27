#!/usr/bin/env python3
"""
台风山竹数据可视化 - 互动演示GIF版本
展示点击效果、信息框和水波纹动画的完整演示
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
output_file = os.path.join(parent_dir, 'assets', 'typhoon_interactive_demo.gif')

print(f"正在读取数据文件: {data_file}")
print(f"交互演示GIF将保存到: {output_file}")

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

# 翻译字典
station_translations = {
    '黄麻角(赤柱)': 'Wong Ma Kok (Stanley)', '中环码头': 'Central Pier', '长洲': 'Cheung Chau',
    '青衣': 'Tsing Yi', '打鼓岭': 'Ta Kwu Ling', '大埔': 'Tai Po', '赤鱲角': 'Chek Lap Kok',
    '天星码头': 'Star Ferry', '西贡': 'Sai Kung', '沙田': 'Sha Tin', '屯门': 'Tuen Mun',
    '大美督': 'Tai Mei Tuk', '将军澳': 'Tseung Kwan O', '元朗公园': 'Yuen Long Park',
    '上水': 'Sheung Shui', '石岗': 'Shek Kong', '京士柏': 'King\'s Park',
    '黄竹坑': 'Wong Chuk Hang', '跑马地': 'Happy Valley', '北角': 'North Point',
    '观塘': 'Kwun Tong', '启德跑道公园': 'Kai Tak Runway Park', '红磡': 'Hung Hom',
    '尖沙咀': 'Tsim Sha Tsui', '湿地公园': 'Wetland Park', '流浮山': 'Lau Fau Shan',
    '香港公园': 'Hong Kong Park', '香港仔': 'Aberdeen', '筲箕湾': 'Shau Kei Wan'
}

direction_translations = {
    '东': 'E', '西': 'W', '南': 'S', '北': 'N', '-': '-',
    '东南': 'SE', '西南': 'SW', '东北': 'NE', '西北': 'NW',
    '东南东': 'ESE', '西南西': 'WSW', '东北东': 'ENE', '西北西': 'WNW'
}

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
fig, ax = plt.subplots(figsize=(12, 10))
fig.patch.set_facecolor("black")
ax.set_facecolor("black")
ax.axis("off")

# 添加标题
fig.suptitle('TYPHOON MANGKHUT - INTERACTIVE WIND VISUALIZATION', 
             fontsize=18, 
             fontweight='bold', 
             color='white', 
             y=0.95,
             fontfamily='monospace')

# 添加演示说明
ax.text(0.5, 0.92, 'Interactive Demo: Click Effects & Station Information Display', 
        transform=fig.transFigure, 
        fontsize=12, 
        color='lightgray', 
        ha='center',
        fontfamily='monospace',
        alpha=0.8,
        style='italic')

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

# 信息显示框 - 使用和原始程序相同的样式
annotation = ax.annotate(
    "",
    xy=(0, 0), xytext=(0.5, 0.5),
    textcoords="axes fraction",
    bbox=dict(boxstyle="round,pad=0.8", fc="lightyellow", alpha=0.95, edgecolor="white", linewidth=2),
    fontsize=12,
    color="black",
    ha="center",
    va="center"
)
annotation.set_visible(False)

# 动画变量
frame_count = 0
ripple_circles = []
click_sequence = [
    {'frame': 80, 'station_idx': 2, 'duration': 60},    # 点击长洲
    {'frame': 200, 'station_idx': 5, 'duration': 60},   # 点击大埔  
    {'frame': 320, 'station_idx': 8, 'duration': 60},   # 点击沙田
]
current_click = None
click_frame = 0
info_alpha = 0.0
ripple_active = False
ripple_frame = 0
ripple_center = (0, 0)

def update(frame):
    global frame_count, current_click, click_frame, info_alpha, ripple_active, ripple_frame, ripple_center, ripple_circles
    
    frame_count = frame
    
    # 使用和原始程序相同的运动模式：半径震荡而不是旋转
    new_x, new_y = [], []
    for i in range(N):
        # 基准半径
        base_r = radii[i]
        # 每个点有不同的相位
        phase = i * np.pi/8
        # 半径在 ±15% 范围内震荡
        r = base_r * (1 + 0.15 * np.sin(frame/20 + phase))
        new_x.append(r * np.cos(angles[i]))
        new_y.append(r * np.sin(angles[i]))
    
    # 呼吸效果（圆点大小变化）- 使用和原始程序相同的参数
    new_sizes = original_sizes * (1 + 0.2 * np.sin(frame/15))
    
    # 检查是否触发新的点击
    for click_event in click_sequence:
        if frame == click_event['frame']:
            current_click = click_event
            click_frame = 0
            idx = click_event['station_idx']
            ripple_center = (new_x[idx], new_y[idx])
            ripple_active = True
            ripple_frame = 0
            
            # 设置信息内容
            station_name = stations[idx]
            wind_speed = speeds[idx]
            wind_dir = wind_dirs[idx]
            time_str = times[idx]
            
            english_station = station_translations.get(station_name, station_name)
            english_direction = direction_translations.get(wind_dir, wind_dir)
            
            annotation.set_text(
                f"STATION: {english_station}\n"
                f"WIND SPEED: {wind_speed} km/h\n"  
                f"DIRECTION: {english_direction}\n"
                f"TIME: {time_str}"
            )
            break
    
    # 处理当前点击效果
    if current_click:
        click_frame += 1
        duration = current_click['duration']
        
        if click_frame <= duration:
            # 信息框淡入淡出效果 - 使用和原始程序相同的逻辑
            if click_frame < 20:       # 前20帧 → 渐入
                info_alpha = click_frame / 20
            elif click_frame < 100:    # 中间保持
                info_alpha = 1.0
            else:                      # 渐出
                info_alpha = max(0, 1 - (click_frame-100)/30)
            
            # 更新信息框透明度
            annotation.set_visible(True)
            annotation.set_alpha(info_alpha)
            bbox_props = dict(
                boxstyle="round,pad=0.8",
                fc="lightyellow",
                alpha=info_alpha * 0.95,
                edgecolor="white",
                linewidth=2
            )
            annotation.set_bbox(bbox_props)
            
            # 高亮被点击的点 - 使用和原始程序相同的效果
            idx = current_click['station_idx']
            highlight_factor = 1.5 + 0.3 * np.sin(frame/2)  # 使用frame而不是click_frame
            new_sizes[idx] *= highlight_factor
        else:
            # 点击效果结束
            current_click = None
            click_frame = 0
            info_alpha = 0.0
            annotation.set_visible(False)
    
    # 处理水波纹效果 - 使用和原始程序完全相同的逻辑
    # 清除之前的波纹圆圈
    for circle in ripple_circles:
        if circle in ax.patches:
            circle.remove()
    ripple_circles.clear()
    
    if ripple_active:
        ripple_frame += 1
        # 创建多层波纹效果
        for i in range(3):  # 3层波纹
            delay = i * 8  # 每层波纹延迟8帧
            if ripple_frame > delay:
                progress = (ripple_frame - delay) / 40.0  # 40帧完成一个波纹
                if progress <= 1.0:
                    radius = progress * 60  # 最大半径60
                    alpha = 0.8 * (1 - progress)  # 透明度逐渐减少
                    
                    circle = plt.Circle(
                        ripple_center, 
                        radius,
                        fill=False,
                        edgecolor='cyan',
                        linewidth=3 - i * 0.5,  # 外层波纹更细
                        alpha=alpha
                    )
                    ax.add_patch(circle)
                    ripple_circles.append(circle)
        
        # 50帧后结束波纹效果
        if ripple_frame >= 50:
            ripple_active = False
            ripple_frame = 0
    
    # 更新散点图
    scat.set_offsets(np.column_stack([new_x, new_y]))
    scat.set_sizes(new_sizes)
    
    return [scat, annotation] + ripple_circles

print("开始生成交互演示GIF...")
print("这个版本将展示：")
print("- 基础动画效果（呼吸、旋转）")
print("- 自动模拟点击3个不同气象站")
print("- 信息框的淡入淡出效果")
print("- 水波纹扩散动画")
print("- 被点击点的高亮闪烁效果")
print("请耐心等待...")

# 创建更长的动画来展示完整的交互序列
ani = FuncAnimation(fig, update, frames=400, interval=100, blit=False)

# 导出GIF
ani.save(output_file, writer="pillow", fps=10, dpi=80)

print(f"交互演示GIF导出完成！")
print(f"文件位置: {output_file}")
print(f"文件大小: {os.path.getsize(output_file) / 1024 / 1024:.2f} MB")
print("这个GIF展示了完整的交互功能，包括点击效果和信息显示！")

plt.close()