# scripts/visualize_news.py
# Візуалізація новин про Audi

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

print("🎨 Запуск візуалізації даних...")

# --- Налаштування ---
DATA_FILE = "C:/Users/iryna/Desktop/audi_project/data/audi_news.csv"
OUTPUT_DIR = "C:/Users/iryna/Desktop/audi_project/outputs"

# Створити папку для графіків якщо не існує
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Завантаження даних ---
try:
    df = pd.read_csv(DATA_FILE)
    print(f"✅ Завантажено {len(df)} записів")
except FileNotFoundError:
    print("❌ Файл не знайдено! Спочатку запустіть collect_news.py")
    # Створюємо тестові дані для демонстрації
    df = pd.DataFrame([
        {'Заголовок': 'Audi announces new EV strategy for 2026', 'Дата_збору': '2026-01-15 10:00', 'Джерело': 'Reuters', 'Ключові_слова': 'Audi, EV, Strategy'},
        {'Заголовок': 'Audi partners with CATL for batteries', 'Дата_збору': '2026-01-14 14:30', 'Джерело': 'Reuters', 'Ключові_слова': 'Audi, Battery, Partnership'},
        {'Заголовок': 'Chinese EV makers expand in Europe', 'Дата_збору': '2026-01-13 09:15', 'Джерело': 'Bloomberg', 'Ключові_слова': 'China, EV, Europe'},
        {'Заголовок': 'Audi Q6 e-tron sales exceed expectations', 'Дата_збору': '2026-01-12 16:45', 'Джерело': 'Reuters', 'Ключові_слова': 'Audi, Sales, Q6'},
        {'Заголовок': 'EU tariffs on Chinese cars under review', 'Дата_збору': '2026-01-11 11:20', 'Джерело': 'FT', 'Ключові_слова': 'EU, Tariffs, China'},
        {'Заголовок': 'Audi invests €2B in electric platform', 'Дата_збору': '2026-01-10 08:00', 'Джерело': 'Reuters', 'Ключові_слова': 'Audi, Investment, EV'},
    ])
    print("💡 Використовуємо тестові дані")

# --- Підготовка даних ---
# Додаємо колонку "Згадка Audi"
df['Згадка_Audi'] = df['Заголовок'].str.contains('Audi', case=False, na=False)

# Групуємо за датою (якщо є нормальні дати)
df['Дата'] = pd.to_datetime(df['Дата_збору'], errors='coerce').dt.date

print(f"📊 Згадки Audi: {df['Згадка_Audi'].sum()} з {len(df)} новин")

# =============================================================================
# 📈 ГРАФІК 1: Частота згадок "Audi" (Matplotlib)
# =============================================================================
print("📊 Створюємо графік частоти згадок...")

fig1, ax = plt.subplots(figsize=(10, 6))

# Дані для графіка
categories = ['Згадки Audi', 'Інші новини']
values = [df['Згадка_Audi'].sum(), (~df['Згадка_Audi']).sum()]
colors = ['#0066cc', '#cccccc']  # Audi blue + gray

# Створення bar chart
bars = ax.bar(categories, values, color=colors, edgecolor='black')

# Додавання значень на стовпчики
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}', ha='center', va='bottom', fontsize=12)

# Оформлення
ax.set_title('🔍 Частота згадок "Audi" у зібраних новинах', fontsize=14, fontweight='bold')
ax.set_ylabel('Кількість новин')
ax.set_xlabel('Категорія')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Збереження
plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/audi_mentions_bar.png', dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Збережено: {OUTPUT_DIR}/audi_mentions_bar.png")

# =============================================================================
# 🥧 ГРАФІК 2: Джерела новин (Plotly - інтерактивний)
# =============================================================================
print("🥧 Створюємо діаграму джерел...")

source_counts = df['Джерело'].value_counts().reset_index()
source_counts.columns = ['Джерело', 'Кількість']

fig2 = px.pie(
    source_counts, 
    values='Кількість', 
    names='Джерело',
    title='📰 Розподіл новин за джерелами',
    color_discrete_sequence=px.colors.qualitative.Set2,
    hole=0.4  # Donut chart style
)

# Додавання відсотків
fig2.update_traces(textposition='inside', textinfo='percent+label')

# Оформлення
fig2.update_layout(
    height=500,
    width=700,
    title_x=0.5,
    showlegend=True,
    font=dict(family='Arial', size=12)
)

# Збереження
fig2.write_html(f'{OUTPUT_DIR}/sources_pie.html')
fig2.write_image(f'{OUTPUT_DIR}/sources_pie.png', width=700, height=500)
print(f"✅ Збережено: {OUTPUT_DIR}/sources_pie.html (інтерактивний)")

# =============================================================================
# 🗓️ ГРАФІК 3: Таймлайн публікацій
# =============================================================================
print("🗓️ Створюємо таймлайн...")

# Групуємо за датою
if df['Дата'].notna().any():
    timeline_data = df.groupby('Дата').size().reset_index(name='Кількість')
    timeline_data['Дата'] = pd.to_datetime(timeline_data['Дата'])
    
    fig3 = px.line(
        timeline_data,
        x='Дата',
        y='Кількість',
        title='📅 Динаміка публікацій новин',
        markers=True,
        line_shape='spline'
    )
    
    fig3.update_layout(
        xaxis_title='Дата',
        yaxis_title='Кількість новин',
        height=400,
        width=800,
        title_x=0.5
    )
    
    fig3.write_html(f'{OUTPUT_DIR}/timeline.html')
    fig3.write_image(f'{OUTPUT_DIR}/timeline.png', width=800, height=400)
    print(f"✅ Збережено: {OUTPUT_DIR}/timeline.html")
else:
    print("⚠️ Недостатньо даних для таймлайну")

# =============================================================================
# 📋 ГРАФІК 4: Хмарина ключових слів (текстова візуалізація)
# =============================================================================
print("🔑 Створюємо аналіз ключових слів...")

# Розбиваємо ключові слова та рахуємо частоту
all_keywords = []
for keywords in df['Ключові_слова'].dropna():
    all_keywords.extend([k.strip() for k in keywords.split(',')])

keyword_counts = pd.Series(all_keywords).value_counts().head(10)

fig4 = px.bar(
    x=keyword_counts.values,
    y=keyword_counts.index,
    orientation='h',
    title='🔑 Топ-10 ключових слів у новинах',
    labels={'x': 'Частота', 'y': 'Ключове слово'},
    color=keyword_counts.values,
    color_continuous_scale='Blues'
)

fig4.update_layout(
    height=500,
    width=700,
    title_x=0.5,
    showlegend=False
)

fig4.write_html(f'{OUTPUT_DIR}/keywords_bar.html')
fig4.write_image(f'{OUTPUT_DIR}/keywords_bar.png', width=700, height=500)
print(f"✅ Збережено: {OUTPUT_DIR}/keywords_bar.html")

# =============================================================================
# 📊 ЗВІТ: Коротка статистика
# =============================================================================
print("\n" + "="*60)
print("📋 СТАТИСТИКА ЗБРАНИХ ДАНИХ")
print("="*60)
print(f"📰 Всього новин: {len(df)}")
print(f"🚗 Згадки Audi: {df['Згадка_Audi'].sum()} ({df['Згадка_Audi'].mean()*100:.1f}%)")
print(f"📡 Унікальних джерел: {df['Джерело'].nunique()}")
print(f"🔑 Унікальних ключових слів: {len(set(all_keywords))}")
print(f"📅 Діапазон дат: {df['Дата'].min()} — {df['Дата'].max()}")
print("="*60)

# =============================================================================
# 💾 Збереження підготовлених даних
# =============================================================================
df.to_csv(f'{OUTPUT_DIR}/processed_news.csv', index=False, encoding='utf-8-sig')
print(f"\n💾 Оброблені дані: {OUTPUT_DIR}/processed_news.csv")

print("\n🎨 Візуалізація завершена! Графіки у папці: outputs/")
print("🔗 Відкрийте .html файли у браузері для інтерактивного перегляду")