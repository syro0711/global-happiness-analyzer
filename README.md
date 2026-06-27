# 🌍 Global Happiness Analyzer

An interactive dashboard analyzing global happiness factors with predictive modeling capabilities. This project compares Indonesia's performance against the world's top 5 happiest countries and provides data-driven insights for policy recommendations.

![Streamlit](https://img.shields.io/badge/Streamlit-1.35.0-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2.2-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22.0-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [Methodology](#methodology)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## ✨ Features

### 🎯 **Multi-Dimensional Analysis**
- **Radar Chart Visualization**: Compare 10+ dimensions of happiness including GDP, social support, health expectancy, freedom, generosity, corruption perception, internet penetration, and healthcare quality
- **Country Comparison**: Side-by-side analysis of Indonesia vs Top 5 happiest countries (Finland, Denmark, Switzerland, Iceland, Netherlands)

### 🔮 **Predictive Engine (What-If Analysis)**
- Interactive sliders to simulate policy impacts
- Real-time projection of happiness score changes
- Scenario modeling for:
  - Economic growth (GDP)
  - Anti-corruption measures
  - Healthcare reform
  - Income inequality reduction
  - Education investment

### 📊 **Deep-Dive Factor Analysis**
- **Scatter Plots**: Explore correlations between external factors (Gini coefficient, crime rates, internet usage) and happiness
- **Correlation Heatmap**: Visualize relationships between all variables using Pearson correlation
- **Trend Analysis**: Historical data visualization for key indicators

### 🎨 **Interactive Dashboard**
- Clean, professional UI built with Streamlit
- Responsive design for desktop and mobile
- Downloadable insights and visualizations

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/global-happiness-analyzer.git
   cd global-happiness-analyzer