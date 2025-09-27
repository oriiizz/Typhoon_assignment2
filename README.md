# Typhoon Mangkhut - Artistic Wind Visualization

## Project Introduction

This project transforms the meteorological station data of Typhoon Mangkhut (2018, Hong Kong) into an artistic visualization animation.
By turning raw wind data into a dynamic display, it captures the power of natural forces while adding breathing-like rhythms and ripple effects, exploring the boundary between data visualization and artistic expression.

## Data Source

**Source:** Hong Kong Observatory (HKO)

**Dataset Details:**
- **Event:** Typhoon Mangkhut (September 2018)
- **Stations:** 28 meteorological stations across Hong Kong
- **Metrics:** Maximum gust wind speed, wind direction, and observation time

**Data Processing:**
- Scraped from official HKO HTML tables
- Processed and cleaned using BeautifulSoup + pandas
- Filtered valid wind speed records (> 0 km/h)

## Creativity & Artistic Design

This project is more than a traditional wind speed chart — it is a data-driven artistic animation:

**Spatial Layout:**
- Each meteorological station is represented as a circle point, distributed radially
- The radius is determined by wind speed (higher speed → farther from center)

**Visual Encoding:**
- Color gradient (viridis colormap) → wind intensity
- Circle size → gust strength

**Artistic Effects:**
- **Breathing effect:** all points gently oscillate, symbolizing air movement
- **Interactive ripple:** clicking on a station triggers a ripple-like expansion, representing the shockwave of strong winds
- **Fading annotation:** clicked station info (location, wind speed, wind direction, time) appears in the center, fades in → stays → fades out

Through this design, the dataset is transformed from raw numbers into a scientific yet artistic dynamic piece.

## How to Run

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/oriiizz/Typhoon_assignment2.git
   cd Typhoon_assignment2
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the visualization:**
   ```bash
   python src/typhoon_visualization.py
   ```

### Interactive Controls
- **Click on any station dot** → View detailed wind information
- **Station info display** → Name, wind speed, direction, and time
- **Visual effects** → Water ripple animation + highlighted station
- **Smooth transitions** → Fade-in/out information display

## Demo & Features

### Interactive Demonstration
![Interactive Demo](assets/typhoon_interactive_demo.gif)

*Complete interactive demonstration showing click effects, station information display, and water ripple animations*

### Before & After Comparison

| Basic View | Click Effect |
|------------|-------------|
| ![Basic View](assets/screenshot_basic.png) | ![Click Effect](assets/screenshot_clicked.png) |

### Key Interactive Features
- **Click Response**: Click any station dot to view detailed information
- **Water Ripple Effect**: Beautiful expanding circles simulate wind impact  
- **Information Display**: Station name, wind speed, direction, and time
- **Visual Feedback**: Highlighted dots with smooth fade-in/out effects
- **Breathing Animation**: Continuous gentle movement simulating air flow

### Export My Own Media

**Generate Interactive Demo GIF:**
```bash
python src/export_interactive_demo.py
# Creates: assets/typhoon_interactive_demo.gif (6.9MB, 20 FPS)
```

**Create Static Screenshots:**
```bash
python src/generate_screenshots.py  
# Creates: assets/screenshot_basic.png & screenshot_clicked.png
```

## Project Structure

```
Typhoon/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── assets/                            # Generated media files
│   ├── typhoon_interactive_demo.gif       # Interactive demo (6.9MB)
│   ├── screenshot_basic.png               # Basic view screenshot
│   └── screenshot_clicked.png             # Click effect screenshot
├── data/                              # Source data files
│   ├── typhoon_mangkhut.html               # HKO weather data (28 stations)
│   └── wind_timeseries.csv                # Time series data
└── src/                               # Source code
    ├── typhoon_visualization.py           # Main interactive program
    ├── export_interactive_demo.py         # GIF exporter (20 FPS, optimized)
    └── generate_screenshots.py            # Screenshot generator
```

## Summary

This project transforms Typhoon Mangkhut wind speed data into an **artistic interactive visualization** that merges data science with creative design.

**Key Achievements:**
- **Data-driven Art**: Converts raw meteorological data into aesthetic visual experience
- **Interactive Design**: Click-responsive interface with smooth animations
- **Artistic Expression**: Breathing effects and ripple animations symbolize natural forces
- **Scientific Accuracy**: Maintains authentic wind speed and direction data

The visualization reflects real wind distribution patterns while expressing the dynamic beauty of natural forces through responsive, animated design.