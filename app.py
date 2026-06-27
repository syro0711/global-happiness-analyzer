import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

st.set_page_config(page_title="Global Happiness Analyzer V3", layout="wide", page_icon="🌍")

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'Master_Happiness_Dataset.csv')
hist_path = os.path.join(script_dir, 'Historical_CPI_Data.csv')

@st.cache_data
def load_data():
    if not os.path.exists(csv_path):
        st.error("❌ File Master_Happiness_Dataset.csv tidak ditemukan!")
        st.stop()
    df = pd.read_csv(csv_path)
    # Konversi numerik
    num_cols = ['Ladder score', 'Logged GDP per capita', 'Social support', 'Healthy life expectancy', 
                'Freedom to make life choices', 'Generosity', 'Perceptions of corruption',
                'Gini_Index', 'Internet_Pct', 'Literacy_Rate', 'Healthcare_Score', 
                'Unemp_Rate', 'Quality_of_Life_Index', 'Safety_Index', 'Pollution_Index',
                'Crime_Index', 'Safety_Index_Crime', 'CPI_Latest', 'Edu_Exp_Pct_GDP']
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

@st.cache_data
def load_hist_data():
    if os.path.exists(hist_path):
        return pd.read_csv(hist_path)
    return pd.DataFrame()

df = load_data()
hist_df = load_hist_data()

st.sidebar.title("🌍 Global Happiness Analyzer")
st.sidebar.markdown("**V3: Comprehensive Analysis**")
page = st.sidebar.radio("Menu Dashboard", [
    "1. 🏆 The Global Stage",
    "2. 🔮 Predictive Engine",
    "3. 📊 Deep-Dive Analysis",
    "4. 🚨 Crime, Safety & Quality of Life",
    "5. 📜 Historical Corruption Trend"
])

TOP_5 = ['Finland', 'Denmark', 'Switzerland', 'Iceland', 'Netherlands']
FOCUS_COUNTRIES = TOP_5 + ['Indonesia']

# ==========================================
# HALAMAN 1: RADAR CHART
# ==========================================
if page == "1. 🏆 The Global Stage":
    st.title("🏆 The Global Stage: Top 5 vs Indonesia")
    st.markdown("Membandingkan **10 dimensi kesejahteraan** (termasuk Safety & Pollution).")
    
    df_focus = df[df['Country name'].isin(FOCUS_COUNTRIES)].copy()
    
    features = ['Logged GDP per capita', 'Social support', 'Healthy life expectancy',
                'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']
    
    # Tambahkan fitur baru jika ada
    if 'Safety_Index_Crime' in df.columns: features.append('Safety_Index_Crime')
    if 'Pollution_Index' in df.columns: features.append('Pollution_Index')
    if 'Gini_Index' in df.columns: features.append('Gini_Index')
    if 'Healthcare_Score' in df.columns: features.append('Healthcare_Score')
        
    for feat in features:
        if feat in df.columns:
            min_val = df[feat].min()
            max_val = df[feat].max()
            # Inversi untuk Gini dan Pollution (semakin rendah semakin baik)
            if feat in ['Gini_Index', 'Pollution_Index']:
                df_focus[f'{feat}_norm'] = 1 - ((df_focus[feat] - min_val) / (max_val - min_val + 1e-5))
            else:
                df_focus[f'{feat}_norm'] = (df_focus[feat] - min_val) / (max_val - min_val + 1e-5)
        else:
            df_focus[f'{feat}_norm'] = 0.5
            
    norm_cols = [f'{feat}_norm' for feat in features]
    theta_cols = [feat.replace('_', ' ').replace('Gini Index', 'Equality').replace('Pollution Index', 'Clean Air').title() for feat in features]
    theta_cols.append(theta_cols[0])
    
    country_colors = {
        'Finland': '#1f77b4', 'Denmark': '#ff7f0e', 'Switzerland': '#2ca02c',
        'Iceland': '#d62728', 'Netherlands': '#9467bd', 'Indonesia': '#ffbf00'
    }
    
    fig = go.Figure()
    for country in FOCUS_COUNTRIES:
        row = df_focus[df_focus['Country name'] == country]
        if not row.empty:
            values = row[norm_cols].iloc[0].tolist()
            values.append(values[0])
            is_idn = country == 'Indonesia'
            fig.add_trace(go.Scatterpolar(
                r=values, theta=theta_cols, fill='toself', name=country,
                fillcolor=country_colors.get(country, 'gray'),
                line=dict(color=country_colors.get(country, 'gray'), width=4 if is_idn else 2),
                opacity=0.5 if is_idn else 0.2
            ))

    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), height=650)
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("""
    **💡 Insight:** Indonesia (Kuning) sangat kuat di **Generosity** dan **Social Support**. 
    Namun, kita tertinggal jauh di **Clean Air (Pollution)**, **Safety**, dan **Equality (Gini)** dibandingkan negara Nordik.
    """)

# ==========================================
# HALAMAN 2: PREDICTIVE ENGINE
# ==========================================
elif page == "2. 🔮 Predictive Engine":
    st.title("🔮 Predictive Engine: Simulasi Kebijakan")
    idn_data = df[df['Country name'] == 'Indonesia']
    if idn_data.empty: st.stop()
    base_score = float(idn_data['Ladder score'].iloc[0])
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader(f"Skor Aktual Indonesia: **{base_score:.3f}**")
        pct_gdp = st.slider("📈 Pertumbuhan Ekonomi", -20, 50, 15)
        pct_corruption = st.slider("🛡️ Pemberantasan Korupsi", -20, 100, 30)
        pct_health = st.slider("🏥 Reformasi Kesehatan", -10, 50, 20)
        pct_ineq = st.slider("⚖️ Penurunan Ketimpangan (Gini)", -50, 0, -15)
        
    with col2:
        delta = (pct_gdp/100)*0.15 + (pct_corruption/100)*0.25 + (pct_health/100)*0.20 + (pct_ineq/100)*-0.15
        predicted_score = base_score + delta
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=predicted_score,
            title={'text': "Proyeksi Skor"},
            delta={'reference': base_score, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge={'axis': {'range': [0, 10]}, 'bar': {'color': "darkblue"},
                   'steps': [{'range': [0, 4], 'color': "#ffcccc"}, {'range': [4, 6], 'color': "#ffffcc"}, {'range': [6, 10], 'color': "#ccffcc"}]}
        ))
        st.plotly_chart(fig_gauge, use_container_width=True)

# ==========================================
# HALAMAN 3: DEEP-DIVE
# ==========================================
elif page == "3. 📊 Deep-Dive Analysis":
    st.title("📊 Deep-Dive: Korelasi Faktor")
    tab1, tab2 = st.tabs([" Scatter Plot", "🌡️ Heatmap"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Gini vs Kebahagiaan")
            if 'Gini_Index' in df.columns:
                df_plot = df.dropna(subset=['Gini_Index', 'Ladder score'])
                fig = px.scatter(df_plot, x='Gini_Index', y='Ladder score', color='Regional indicator', 
                                 hover_name='Country name', trendline="ols")
                st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("Crime Index vs Kebahagiaan")
            if 'Crime_Index' in df.columns:
                df_plot = df.dropna(subset=['Crime_Index', 'Ladder score'])
                fig = px.scatter(df_plot, x='Crime_Index', y='Ladder score', color='Regional indicator', 
                                 hover_name='Country name', trendline="ols")
                st.plotly_chart(fig, use_container_width=True)
                
    with tab2:
        cols = ['Ladder score', 'Logged GDP per capita', 'Gini_Index', 'Crime_Index', 'Safety_Index_Crime', 'Pollution_Index', 'CPI_Latest']
        cols = [c for c in cols if c in df.columns]
        df_corr = df[cols].dropna()
        fig = px.imshow(df_corr.corr(), text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# HALAMAN 4: CRIME, SAFETY & QOL
# ==========================================
elif page == "4. 🚨 Crime, Safety & Quality of Life":
    st.title("🚨 Crime, Safety & Quality of Life Analysis")
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Crime Index vs Happiness")
        if 'Crime_Index' in df.columns:
            df_plot = df.dropna(subset=['Crime_Index', 'Ladder score'])
            fig = px.scatter(df_plot, x='Crime_Index', y='Ladder score', color='Regional indicator', 
                             size='Logged GDP per capita', hover_name='Country name', trendline="ols",
                             title="Negara dengan kejahatan tinggi cenderung tidak bahagia")
            st.plotly_chart(fig, use_container_width=True)
            
    with c2:
        st.subheader("Safety Index vs Happiness")
        if 'Safety_Index_Crime' in df.columns:
            df_plot = df.dropna(subset=['Safety_Index_Crime', 'Ladder score'])
            fig = px.scatter(df_plot, x='Safety_Index_Crime', y='Ladder score', color='Regional indicator', 
                             size='Logged GDP per capita', hover_name='Country name', trendline="ols",
                             title="Rasa aman berbanding lurus dengan kebahagiaan")
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Perbandingan Safety & Crime: Indonesia vs Top 5")
    if 'Crime_Index' in df.columns and 'Safety_Index_Crime' in df.columns:
        df_comp = df[df['Country name'].isin(FOCUS_COUNTRIES)][['Country name', 'Crime_Index', 'Safety_Index_Crime', 'Ladder score']].dropna()
        st.dataframe(df_comp, use_container_width=True)

# ==========================================
# HALAMAN 5: HISTORICAL CORRUPTION
# ==========================================
elif page == "5. 📜 Historical Corruption Trend":
    st.title("📜 Historical Corruption Trend (CPI)")
    st.markdown("Melacak tren skor persepsi korupsi (CPI) dari tahun ke tahun. *Semakin tinggi skor, semakin bersih.*")
    
    if not hist_df.empty:
        # Filter negara fokus
        hist_focus = hist_df[hist_df['Country'].isin(FOCUS_COUNTRIES)]
        
        if not hist_focus.empty:
            fig = px.line(hist_focus, x='Year_Index', y='CPI_Score', color='Country',
                          markers=True, line_shape='spline',
                          title="Tren Skor Korupsi (CPI) 5 Tahun Terakhir",
                          color_discrete_map={'Indonesia': '#ffbf00', 'Finland': '#1f77b4', 'Denmark': '#ff7f0e', 
                                              'Switzerland': '#2ca02c', 'Iceland': '#d62728', 'Netherlands': '#9467bd'})
            fig.update_layout(xaxis_title="Tahun (Indeks)", yaxis_title="Skor CPI (Makin Tinggi = Makin Bersih)", height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("""
            **💡 Insight Kritis:** 
            Perhatikan garis **Indonesia (Kuning)**. Trennya cenderung **menurun/stagnan** (skor memburuk). 
            Sementara itu, negara Nordik seperti **Finland** dan **Denmark** mempertahankan skor tinggi yang stabil. 
            Ini membuktikan bahwa pemberantasan korupsi di Indonesia masih menghadapi tantangan besar dan belum menunjukkan tren perbaikan yang konsisten.
            """)
        else:
            st.warning("Data historis untuk negara fokus tidak ditemukan.")
    else:
        st.warning("File Historical_CPI_Data.csv tidak ditemukan.")