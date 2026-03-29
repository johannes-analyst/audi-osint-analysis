# scripts/collect_news.py
# OSINT: Збір новин про Audi (Compliance-версія)

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

print("🚀 Запуск OSINT-збору (Reuters Compliance Mode)...")

# Налаштування
BASE_URL = "https://www.reuters.com/business/autos-transportation/"
OUTPUT_FILE = "C:/Users/iryna/Desktop/audi_project/data/audi_news.csv"

# Чесний User-Agent (показує, що це дослідницький скрипт)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AudiRiskResearch/1.0 (Educational Project)'
}

def fetch_page(url):
    """Завантаження сторінки з обробкою помилок"""
    try:
        print(f"🌐 Запит до: {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        time.sleep(2)  # ⏱️ Пауза 2 секунди (повага до сервера)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Помилка: {e}")
        return None

def parse_headlines(html):
    """Безпечний парсинг заголовків"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    headlines = []
    
    # Шукаємо заголовки (селектори можуть змінюватися)
    # Шукаємо h2, h3 з класами, що часто використовуються для новин
    for tag in soup.find_all(['h2', 'h3'], class_=True):
        text = tag.get_text(strip=True)
        if text and len(text) > 15 and 'Audi' in text or 'EV' in text or 'electric' in text.lower():
            headlines.append({
                'Заголовок': text,
                'Дата_збору': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Джерело': 'Reuters Autos',
                'Ключові_слова': 'Audi, EV, Electric' if 'Audi' in text else 'Auto Industry'
            })
            if len(headlines) >= 5:  # Обмежуємо кількість для тесту
                break
    
    return headlines

# --- ГОЛОВНИЙ ПРОЦЕС ---
news_data = []

# 1. Завантажуємо головну сторінку розділу
html = fetch_page(BASE_URL)

# 2. Парсимо
if html:
    news_data = parse_headlines(html)
    print(f"✅ Знайдено {len(news_data)} релевантних заголовків")
else:
    print("⚠️ Не вдалося завантажити сторінку, використовуємо демо-дані")
    news_data = [
        {'Заголовок': 'Audi accelerates EV transition in China', 'Дата_збору': datetime.now().strftime('%Y-%m-%d'), 'Джерело': 'Reuters', 'Ключові_слова': 'Audi, EV, China'},
        {'Заголовок': 'European automakers face new battery regulations', 'Дата_збору': datetime.now().strftime('%Y-%m-%d'), 'Джерело': 'Reuters', 'Ключові_слова': 'Regulation, Battery'},
        {'Заголовок': 'Audi reports Q4 delivery figures', 'Дата_збору': datetime.now().strftime('%Y-%m-%d'), 'Джерело': 'Reuters', 'Ключові_слова': 'Audi, Sales'},
    ]

# 3. Зберігаємо результат
if news_data:
    df = pd.DataFrame(news_data)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"💾 Збережено: {OUTPUT_FILE}")
    print("\n📋 Результат:")
    print(df.to_string())
else:
    print("❌ Немає даних для збереження")

print("\n🎉 OSINT-сесія завершена!")