import pandas as pd
import numpy as np
import os

print("="*70)
print("🚀 MEMBUAT MASTER DATASET V3 (KOMPREHENSIF + HISTORICAL)")
print("="*70)

# Kamus penyamaan nama negara
map_to_whr = {
    'Russian Federation': 'Russia', 'Korea, Rep.': 'South Korea',
    'Iran, Islamic Rep.': 'Iran', 'Egypt, Arab Rep.': 'Egypt',
    'Venezuela, RB': 'Venezuela', 'Czechia': 'Czech Republic',
    'Turkiye': 'Turkey', 'Cote d\'Ivoire': 'Ivory Coast',
    'Gambia, The': 'Gambia', 'Lao PDR': 'Laos',
    'Kyrgyz Republic': 'Kyrgyzstan', 'Slovak Republic': 'Slovakia',
    'United States': 'United States', 'Syrian Arab Republic': 'Syria',
    'Hong Kong SAR, China': 'Hong Kong', 'Taiwan Province of China': 'Taiwan',
    'Congo, Dem. Rep.': 'DR Congo', 'Congo, Rep.': 'Republic of the Congo',
    'Micronesia, Fed. Sts.': 'Micronesia', 'Bahamas, The': 'Bahamas',
    'Yemen, Rep.': 'Yemen', 'United Kingdom': 'United Kingdom'
}

# 1. WORLD HAPPINESS REPORT 2021 (BASE)
print("\n[1/10] Loading World Happiness Report 2021...")
whr = pd.read_csv('world-happiness-report-2021.csv')
whr['Country name'] = whr['Country name'].replace(map_to_whr)
print(f"   ✅ {len(whr)} negara dimuat")

# 2. GINI INDEX
print("\n[2/10] Loading Gini Index...")
try:
    gini = pd.read_csv('gini_by_country.csv')
    gini['country_name'] = gini['country_name'].replace(map_to_whr)
    gini_df = gini.sort_values('year').drop_duplicates('country_name', keep='last')
    gini_df = gini_df[['country_name', 'value']].rename(columns={'country_name': 'Country name', 'value': 'Gini_Index'})
    print(f"   ✅ {len(gini_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    gini_df = pd.DataFrame()

# 3. INTERNET USERS 2024
print("\n[3/10] Loading Internet Users 2024...")
try:
    inet = pd.read_csv('internet-users-by-country-2024.csv')
    inet['country'] = inet['country'].replace(map_to_whr)
    inet_df = inet[['country', 'InternetUsers_PctOfPopulationUsingInternet']].rename(
        columns={'country': 'Country name', 'InternetUsers_PctOfPopulationUsingInternet': 'Internet_Pct'})
    print(f"   ✅ {len(inet_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    inet_df = pd.DataFrame()

# 4. LITERACY RATE
print("\n[4/10] Loading Literacy Rate...")
try:
    lit = pd.read_csv('Literacy Rate.csv', header=None, names=['S.No', 'Country', 'Literacy Rate', 'Year'])
    lit['Country'] = lit['Country'].replace(map_to_whr)
    lit_df = lit[['Country', 'Literacy Rate']].dropna().rename(columns={'Country': 'Country name', 'Literacy Rate': 'Literacy_Rate'})
    print(f"   ✅ {len(lit_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    lit_df = pd.DataFrame()

# 5. HEALTHCARE SYSTEM PERFORMANCE
print("\n[5/10] Loading Healthcare Performance...")
try:
    hc = pd.read_csv('Healthcare_System_Performance_Dataset.csv', header=None)
    hc.columns = ['Country name', 'Region', 'Income_Level', 'Health_System', 'HC_Score', 'HC_Rank', 'HC_Exp', 'HC_Life_Exp', 'HC_Wait', 'HC_Return', 'HC_Mort', 'HC_Surv', 'HC_Doc', 'HC_Nurse', 'HC_Bed', 'HC_Tech', 'HC_Pharm']
    hc['Country name'] = hc['Country name'].replace(map_to_whr)
    hc_df = hc[['Country name', 'HC_Score']].rename(columns={'HC_Score': 'Healthcare_Score'})
    print(f"   ✅ {len(hc_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    hc_df = pd.DataFrame()

# 6. EMPLOYMENT & GDP
print("\n[6/10] Loading Employment & GDP...")
try:
    emp = pd.read_csv('Employment_Unemployment_GDP_data.csv', header=None)
    emp.columns = ['Country name', 'Year', 'Emp_Agri', 'Emp_Ind', 'Emp_Serv', 'Unemp_Rate', 'GDP']
    emp['Country name'] = emp['Country name'].replace(map_to_whr)
    emp_df = emp.sort_values('Year').drop_duplicates('Country name', keep='last')[['Country name', 'Unemp_Rate', 'Emp_Serv', 'GDP']]
    print(f"   ✅ {len(emp_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    emp_df = pd.DataFrame()

# 7. 🆕 QUALITY OF LIFE 2024
print("\n[7/10] Loading Quality of Life 2024...")
try:
    qol = pd.read_csv('updated_quality_of_life_2024.csv')
    qol['Country'] = qol['Country'].replace(map_to_whr)
    qol_df = qol[['Country', 'Quality_of_Life_Index', 'Safety_Index', 'Health_Care_Index', 'Pollution_Index']].rename(
        columns={'Country': 'Country name'})
    print(f"   ✅ {len(qol_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    qol_df = pd.DataFrame()

# 8. 🆕 CRIME RATE 2024
print("\n[8/10] Loading Crime Rate 2024...")
try:
    crime = pd.read_csv('crime-rate-by-country-2024.csv')
    crime['country'] = crime['country'].replace(map_to_whr)
    crime_df = crime[['country', 'crimeRateByCountry_crimeIndex', 'CrimeRateSafetyIndex']].rename(
        columns={'country': 'Country name', 'crimeRateByCountry_crimeIndex': 'Crime_Index', 'CrimeRateSafetyIndex': 'Safety_Index_Crime'})
    print(f"   ✅ {len(crime_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    crime_df = pd.DataFrame()

# 9. 🆕 HISTORICAL CORRUPTION (CPI)
print("\n[9/10] Loading Historical Corruption Data...")
try:
    hist = pd.read_csv('history.csv', header=None, names=['Rank', 'Country', 'Code', 'Region', 'CPI_Y1', 'CPI_Y2', 'CPI_Y3', 'CPI_Y4', 'CPI_Y5'])
    hist['Country'] = hist['Country'].replace(map_to_whr)
    # Ambil skor terbaru (CPI_Y5) dan rata-rata 5 tahun
    hist_df = hist[['Country', 'CPI_Y5']].rename(columns={'Country': 'Country name', 'CPI_Y5': 'CPI_Latest'})
    # Simpan juga data historis untuk line chart
    hist_melted = hist.melt(id_vars=['Country'], value_vars=['CPI_Y1', 'CPI_Y2', 'CPI_Y3', 'CPI_Y4', 'CPI_Y5'], var_name='Year_Index', value_name='CPI_Score')
    hist_melted['Country'] = hist_melted['Country'].replace(map_to_whr)
    print(f"   ✅ {len(hist_df)} negara (Data Historis CPI)")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    hist_df = pd.DataFrame()
    hist_melted = pd.DataFrame()

# 10. WORLD EDUCATION DATA
print("\n[10/10] Loading World Education Data...")
try:
    edu = pd.read_csv('world-education-data.csv', header=None)
    edu.columns = ['Country', 'Code', 'Year', 'Gov_Exp_Edu', 'Lit_Rate', 'School_Enrol_Prim', 'Pupil_Teach_Prim', 'Pupil_Teach_Sec', 'School_Enrol_Sec', 'School_Enrol_Ter']
    edu['Country'] = edu['Country'].replace(map_to_whr)
    edu_df = edu.sort_values('Year').drop_duplicates('Country', keep='last')[['Country', 'Gov_Exp_Edu']].rename(columns={'Country': 'Country name', 'Gov_Exp_Edu': 'Edu_Exp_Pct_GDP'})
    print(f"   ✅ {len(edu_df)} negara")
except Exception as e:
    print(f"   ⚠️ Error: {e}")
    edu_df = pd.DataFrame()

# ==========================================
# MASTER MERGE
# ==========================================
print("\n" + "="*70)
print("🔗 MELAKUKAN MERGING DATA...")
print("="*70)

master = whr.copy()
for df_right, name in [(gini_df, 'Gini'), (inet_df, 'Internet'), (lit_df, 'Literacy'), 
                       (hc_df, 'Healthcare'), (emp_df, 'Employment'), (qol_df, 'Quality of Life'),
                       (crime_df, 'Crime Rate'), (hist_df, 'CPI Latest'), (edu_df, 'Education')]:
    if not df_right.empty:
        master = master.merge(df_right, on='Country name', how='left')
        print(f"   ✅ Merged {name}")

# Simpan Master Dataset
master.to_csv('Master_Happiness_Dataset.csv', index=False)

# Simpan Data Historis CPI untuk Line Chart
if not hist_melted.empty:
    hist_melted.to_csv('Historical_CPI_Data.csv', index=False)
    print("   ✅ Historical CPI Data disimpan ke Historical_CPI_Data.csv")

print("\n" + "="*70)
print("🎉 BERHASIL! Master Dataset V3 telah dibuat!")
print("="*70)
print(f"📊 Total negara: {len(master)}")
print(f" Total kolom: {len(master.columns)}")

# Cek Indonesia
idn = master[master['Country name'] == 'Indonesia']
if not idn.empty:
    print(f"\n🇮🇩 DATA INDONESIA:")
    for col in ['Ladder score', 'Gini_Index', 'Internet_Pct', 'Healthcare_Score', 'Crime_Index', 'Safety_Index_Crime', 'CPI_Latest']:
        if col in idn.columns and pd.notna(idn[col].values[0]):
            print(f"   • {col}: {idn[col].values[0]}")