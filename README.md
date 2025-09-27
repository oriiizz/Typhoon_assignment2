# Typhoon Art Visualization

一个基于台风山竹气象数据的艺术化动画可视化项目，展示香港各气象站的风力数据。

## 项目特点

🎨 **艺术化设计**
- 黑色背景的圆形布局
- 根据风速动态调整点的大小和位置
- 流畅的呼吸运动和旋转动画效果

🌪️ **台风数据可视化**
- 基于台风山竹期间的真实气象数据
- 展示各气象站的最高阵风风速
- 包含风向、时间等详细信息

🖱️ **交互功能**
- 点击任意气象站查看详细信息
- 动态高亮和闪烁效果
- 实时动画展示

## 项目结构

```
typhoon-art-viz/
├── data/
│   └── typhoon_mangkhut.html    # 台风山竹气象数据
├── src/
│   └── typhoon_visualization.py # 主可视化脚本
├── requirements.txt             # 项目依赖
├── .venv/                      # Python虚拟环境
└── README.md                   # 项目说明
```

## 安装与运行

### 环境要求

- Python 3.7+
- 推荐使用虚拟环境

### 快速开始

1. **克隆项目**
   ```bash
   git clone https://github.com/oriiizz/Typhoon_assignment2.git
   cd Typhoon_assignment2
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行可视化**
   ```bash
   python src/typhoon_visualization.py
   ```

### 使用虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 运行项目
python src/typhoon_visualization.py

# 退出虚拟环境
deactivate
```

## 技术栈

| 库 | 用途 |
|---|---|
| **pandas** | 数据处理和分析 |
| **beautifulsoup4** | HTML数据解析 |
| **matplotlib** | 绘图和动画制作 |
| **numpy** | 数值计算和数组操作 |

## 功能演示

### 主要功能

- **圆形排列**: 气象站按圆形均匀分布
- **大小映射**: 点的大小反映风速强度
- **动态效果**: 
  - 轻微的呼吸运动（基于正弦波）
  - 整体缓慢旋转
  - 大小波动动画
- **交互响应**: 
  - 鼠标点击显示详细信息
  - 被点击的点会放大闪烁
  - 信息框显示站点名、风速、风向、时间

### 数据说明

项目使用台风山竹（2018年）影响香港期间的气象数据，包括：

- 气象站名称
- 最高阵风风速 (km/h)
- 风向信息
- 记录时间
- 地理位置信息

## 代码结构

```python
# 主要组件
├── 数据读取模块     # 解析HTML中的气象数据
├── 数据处理模块     # 清理和转换数据格式
├── 可视化设置模块   # 配置画布和样式
├── 动画更新函数     # 处理动态效果
├── 交互事件处理     # 响应用户点击
└── 主程序入口      # 启动动画循环
```

## 自定义配置

你可以通过修改以下参数来自定义可视化效果：

```python
# 画布设置
figsize=(10, 10)           # 画布大小
background_color="#111111"  # 背景颜色

# 动画参数
frames=500                 # 动画帧数
interval=80               # 帧间隔（毫秒）

# 视觉效果
point_scale=5             # 点的大小缩放
rotation_speed=0.02       # 旋转速度
breathing_amplitude=0.2   # 呼吸幅度
```

## 许可证

MIT License

## 作者

**oriiizz** - [GitHub](https://github.com/oriiizz)

---

⭐ 如果这个项目对你有帮助，欢迎给个Star！