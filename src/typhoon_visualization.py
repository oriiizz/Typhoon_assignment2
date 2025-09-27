import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import os

# ========== 数据读取 ==========
# 获取脚本所在目录的父目录，然后定位到data文件夹
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
html_file = os.path.join(project_dir, 'data', 'typhoon_mangkhut.html')
with open(html_file, 'r', encoding='utf-8') as f:
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



# ========== 艺术参数 ==========
N = len(stations)
angles = np.linspace(0, 2*np.pi, N, endpoint=False)  # 分布角度
radii = np.log1p(speeds) * 20                       # 半径 ~ 风速

# 初始位置（极坐标转直角坐标）
x = radii * np.cos(angles)
y = radii * np.sin(angles)

colors = plt.cm.viridis(speeds / speeds.max())  # 风速映射颜色
sizes = speeds * 5 + 50                         # 风速映射大小
original_sizes = sizes.copy()                   # 保存原始大小

# ========== 绘图 ==========
fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor("black")  # 图形背景
ax.set_facecolor("black")         # 坐标轴背景
ax.axis("off")  # 去掉坐标轴

# 添加标题
fig.suptitle('TYPHOON MANGKHUT - WIND SPEED VISUALIZATION', 
             fontsize=18, 
             fontweight='bold', 
             color='white', 
             y=0.95,
             fontfamily='monospace')

# 添加操作提示
ax.text(0.5, 0.88, 'Click on any station dot for detailed information', 
        transform=fig.transFigure, 
        fontsize=10, 
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

# 设置显示范围，确保所有点都在画面内
max_radius = np.max(radii) * 1.4  # 考虑最大扩散范围
ax.set_xlim(-max_radius, max_radius)
ax.set_ylim(-max_radius, max_radius)

scat = ax.scatter(x, y, s=sizes, c=colors, alpha=0.8, edgecolors="white", linewidth=0.5, picker=True)

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

click_idx = None
click_frame = 0
text_alpha = 0.0
text_life = 0   # 文字显示寿命计数

# ========== 动画更新函数 ==========
def update(frame):
    global click_idx, click_frame, text_alpha, text_life
    
    # 每个点在基准半径附近做小幅度扩散运动
    new_x, new_y = [], []
    for i in range(N):
        # 基准半径
        base_r = radii[i]
        # 每个点有不同的相位（phase_shift）
        phase = i * np.pi/8
        # 半径在 ±15% 范围内震荡
        r = base_r * (1 + 0.15 * np.sin(frame/20 + phase))
        new_x.append(r * np.cos(angles[i]))
        new_y.append(r * np.sin(angles[i]))
    
    scat.set_offsets(np.c_[new_x, new_y])

    # 呼吸效果（圆点大小变化）
    current_sizes = original_sizes * (1 + 0.2*np.sin(frame/15))
    
    # 点击放大效果
    if click_idx is not None:
        current_sizes[click_idx] *= (1.5 + 0.3*np.sin(frame/2))
        click_frame += 1
        if click_frame > 60:
            click_idx = None
            click_frame = 0
    
    scat.set_sizes(current_sizes)

    # === 控制文字淡入淡出 ===
    if text_life > 0:
        if text_life < 20:       # 前20帧 → 渐入
            text_alpha = text_life / 20
        elif text_life < 100:    # 中间保持
            text_alpha = 1.0
        else:                    # 渐出
            text_alpha = max(0, 1 - (text_life-100)/30)
        
        # 更新文字框的透明度
        bbox_props = dict(
            boxstyle="round,pad=1.0",
            fc="black",
            alpha=text_alpha * 0.8,  # 背景透明度
            edgecolor="cyan",
            linewidth=2
        )
        annotation.set_bbox(bbox_props)
        annotation.set_alpha(text_alpha)
        
        text_life += 1
        if text_alpha <= 0:      # 完全透明后隐藏
            annotation.set_visible(False)
            text_life = 0

    return scat,

# ========== 翻译字典 ==========
direction_translations = {
    '北': 'N', '東北': 'NE', '東': 'E', '東南': 'SE',
    '南': 'S', '西南': 'SW', '西': 'W', '西北': 'NW',
    '東北偏北': 'NNE', '東北偏東': 'ENE',
    '東南偏東': 'ESE', '東南偏南': 'SSE',
    '西南偏南': 'SSW', '西南偏西': 'WSW',
    '西北偏西': 'WNW', '西北偏北': 'NNW',
    '-': 'N/A'  # 处理缺失数据
}

station_translations = {
    '黃麻角(赤柱)': 'Wong Ma Kok (Stanley)',
    '中環碼頭': 'Central Pier',
    '長洲': 'Cheung Chau',
    '長洲泳灘': 'Cheung Chau Beach',
    '青洲': 'Green Island',
    '香港國際機場': 'Hong Kong International Airport',
    '啟德': 'Kai Tak',
    '京士柏': 'King\'s Park',
    '流浮山': 'Lau Fau Shan',
    '北角': 'North Point',
    '平洲': 'Ping Chau',
    '西貢': 'Sai Kung',
    '沙洲': 'Sha Chau',
    '沙螺灣': 'Sha Lo Wan',
    '沙田': 'Sha Tin',
    '石崗': 'Shek Kong',
    '九龍天星碼頭': 'Tsim Sha Tsui Star Ferry Pier',
    '打鼓嶺': 'Ta Kwu Ling',
    '大美督': 'Tai Mei Tuk',
    '大帽山': 'Tai Mo Shan',
    '大埔滘': 'Tai Po Kau',
    '大老山': 'Tate\'s Cairn',
    '將軍澳': 'Tseung Kwan O',
    '青衣島蜆殼油庫': 'Tsing Yi Shell Depot',
    '屯門政府合署': 'Tuen Mun Government Offices',
    '橫瀾島': 'Waglan Island',
    '濕地公園': 'Wetland Park',
    '黃竹坑': 'Wong Chuk Hang'
}

direction_translations = {
    '北': 'N', '東北': 'NE', '東': 'E', '東南': 'SE',
    '南': 'S', '西南': 'SW', '西': 'W', '西北': 'NW',
    '東北偏北': 'NNE', '東北偏東': 'ENE',
    '東南偏東': 'ESE', '東南偏南': 'SSE',
    '西南偏南': 'SSW', '西南偏西': 'WSW',
    '西北偏西': 'WNW', '西北偏北': 'NNW'
}

# ========== 点击事件 ==========
def on_pick(event):
    global annotation, click_idx, click_frame, text_alpha, text_life
    idx = event.ind[0]
    click_idx = idx
    click_frame = 0
    text_alpha = 0.0
    text_life = 1   # 开始计时
    
    station_name = stations[idx]
    wind_speed = speeds[idx]
    wind_dir = wind_dirs[idx]
    time_str = times[idx]
    
    # 翻译站点名称和风向
    english_station = station_translations.get(station_name, station_name)
    english_direction = direction_translations.get(wind_dir, wind_dir)
    
    # 显示信息在画面中央
    annotation.xy = (0, 0)
    annotation.xytext = (0.5, 0.5)
    
    annotation.set_text(
        f"STATION: {english_station}\n"
        f"WIND SPEED: {wind_speed} km/h\n"  
        f"DIRECTION: {english_direction}\n"
        f"TIME: {time_str}"
    )
    annotation.set_visible(True)
    annotation.set_alpha(0.0)  # 初始透明
    annotation.set_fontsize(14)
    annotation.set_color("white")
    annotation.set_family("monospace")  # 使用等宽字体
    annotation.set_bbox(dict(
        boxstyle="round,pad=1.0",
        fc="black",
        alpha=0.0,  # 初始透明
        edgecolor="cyan",
        linewidth=2
    ))
    fig.canvas.draw_idle()

fig.canvas.mpl_connect("pick_event", on_pick)

ani = FuncAnimation(fig, update, frames=500, interval=50, blit=False)
plt.show()