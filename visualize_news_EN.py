# scripts/visualize_news_EN.py (FIXED VERSION)
# Audi OSINT Project - News Visualization (English)

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import os
from datetime import datetime

print("🎨 Starting data visualization...")

# --- Configuration ---
DATA_FILE = "C:/Users/iryna/Desktop/audi_project/data/audi_news.csv"
OUTPUT_DIR = "C:/Users/iryna/Desktop/audi_project/outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Load Data ---
try:
    df = pd.read_csv(DATA_FILE)
    print(f"✅ Loaded {len(df)} records")
except FileNotFoundError:
    print("❌ File not found! Run collect_news.py first")
    exit()

# --- Column Name Mapping (UA → EN) ---
# Автоматично визначаємо назви колонок
column_map = {
    'Заголовок': 'Headline',
    'Headline': 'Headline',
    'Дата_збору': 'Date_Collected',
    'Date_Collected': 'Date_Collected',
    'Джерело': 'Source',
    'Source': 'Source',
    'Ключові_слова': 'Keywords',
    'Keywords': 'Keywords'
}

# Перейменовуємо колонки
df = df.rename(columns=column_map)

# Перевірка чи всі потрібні колонки є
required_columns = ['Headline', 'Source', 'Keywords']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    print(f"❌ Missing columns: {missing}")
    print(f"📋 Available columns: {list(df.columns)}")
    exit()

print(f"📋 Columns: {list(df.columns)}")

# --- Data Preparation ---
df['Mentions_Audi'] = df['Headline'].str.contains('Audi', case=False, na=False)
df['Date'] = pd.to_datetime(df['Date_Collected'], errors='coerce').dt.date

audi_mentions = df['Mentions_Audi'].sum()
total_news = len(df)
audi_percentage = (audi_mentions / total_news * 100) if total_news > 0 else 0

print(f"📊 Audi mentions: {audi_mentions} out of {total_news} news ({audi_percentage:.1f}%)")

# =============================================================================
# 📈 CHART 1: Audi Mention Frequency (Matplotlib)
# =============================================================================
print("📊 Creating mention frequency chart...")

fig1, ax = plt.subplots(figsize=(10, 6))

categories = ['Audi Mentions', 'Other News']
values = [audi_mentions, total_news - audi_mentions]
colors = ['#0066cc', '#cccccc']

bars = ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_title('Frequency of "Audi" Mentions in Collected News', fontsize=14, fontweight='bold', pad=20)
ax.set_ylabel('Number of News Items', fontsize=11)
ax.set_xlabel('Category', fontsize=11)
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.7)
ax.set_axisbelow(True)

ax.text(0.5, max(values) * 0.9, f'{audi_percentage:.1f}% of total', 
        ha='center', fontsize=10, style='italic', 
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/audi_mentions_bar_EN.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Saved: {OUTPUT_DIR}/audi_mentions_bar_EN.png")

# =============================================================================
# 🥧 CHART 2: News Sources Distribution (Plotly)
# =============================================================================
print("🥧 Creating sources distribution chart...")

source_counts = df['Source'].value_counts().reset_index()
source_counts.columns = ['Source', 'Count']

fig2 = px.pie(
    source_counts, 
    values='Count', 
    names='Source',
    title='News Sources Distribution',
    color_discrete_sequence=px.colors.qualitative.Set2,
    hole=0.4
)

fig2.update_traces(
    textposition='inside', 
    textinfo='percent+label',
    textfont_size=11,
    marker=dict(line=dict(color='#000000', width=1.5))
)

fig2.update_layout(
    height=500,
    width=700,
    title_x=0.5,
    title_font_size=14,
    showlegend=True,
    legend_font_size=10,
    font=dict(family='Arial', size=11)
)

fig2.write_html(f'{OUTPUT_DIR}/sources_pie_EN.html')
print(f"✅ Saved interactive: {OUTPUT_DIR}/sources_pie_EN.html")

try:
    fig2.write_image(f'{OUTPUT_DIR}/sources_pie_EN.png', width=700, height=500, scale=2)
    print(f"✅ Saved static: {OUTPUT_DIR}/sources_pie_EN.png")
except Exception as e:
    print(f"⚠️ PNG export failed: {e}")

# =============================================================================
# 🔑 CHART 3: Keywords Analysis
# =============================================================================
print("🔑 Creating keywords analysis chart...")

all_keywords = []
for keywords in df['Keywords'].dropna():
    all_keywords.extend([k.strip() for k in keywords.split(',')])

keyword_counts = pd.Series(all_keywords).value_counts().head(8)

if len(keyword_counts) > 0:
    fig3 = px.bar(
        x=keyword_counts.values,
        y=keyword_counts.index,
        orientation='h',
        title='Top Keywords in Audi-Related News',
        labels={'x': 'Frequency', 'y': 'Keyword'},
        color=keyword_counts.values,
        color_continuous_scale='Blues'
    )

    fig3.update_layout(
        height=450,
        width=700,
        title_x=0.5,
        title_font_size=14,
        showlegend=False,
        font=dict(family='Arial', size=11)
    )

    fig3.write_html(f'{OUTPUT_DIR}/keywords_bar_EN.html')
    fig3.write_image(f'{OUTPUT_DIR}/keywords_bar_EN.png', width=700, height=450, scale=2)
    print(f"✅ Saved: {OUTPUT_DIR}/keywords_bar_EN.png")
else:
    print("⚠️ No keywords data available")

# =============================================================================
# 📋 SUMMARY REPORT
# =============================================================================
print("\n" + "="*60)
print("📊 OSINT ANALYSIS SUMMARY")
print("="*60)
print(f"📰 Total News Articles:     {total_news}")
print(f"🚗 Audi Mentions:           {audi_mentions} ({audi_percentage:.1f}%)")
print(f"📡 Unique News Sources:     {df['Source'].nunique()}")
print(f"🔑 Unique Keywords:         {len(set(all_keywords))}")
print(f"📅 Data Collection Date:    {datetime.now().strftime('%Y-%m-%d')}")
print("="*60)

# =============================================================================
# 💾 Save Processed Data
# =============================================================================
df.to_csv(f'{OUTPUT_DIR}/processed_news_EN.csv', index=False, encoding='utf-8-sig')
print(f"\n💾 Processed data: {OUTPUT_DIR}/processed_news_EN.csv")

print("\n🎨 Visualization complete! Check outputs/ folder")
print("🔗 Open .html files in browser for interactive view")