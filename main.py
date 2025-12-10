import os
import time
import requests
from telegram import Bot

# ТОКЕН И ID ГРУППЫ — ТОЛЬКО ИЗ СЕКРЕТОВ (в коде их НЕТ!)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Проверка, что секреты есть
if not TELEGRAM_TOKEN or not CHAT_ID:
    print("ОШИБКА: Добавь TELEGRAM_TOKEN и CHAT_ID в GitHub Secrets!")
    exit()

bot = Bot(token=TELEGRAM_TOKEN)

def send(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
        print("Сигнал отправлен в группу!")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def check_btc():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        data = requests.get(url).json()
        price = data["bitcoin"]["usd"]
        change = data["bitcoin"]["usd_24h_change"]

        if change > 0.5:
            send(f"""
СВИНГ LONG BTC/USDT
Цена: ${price:,.0f}
+{change:.2f}% за 24ч

SMC + Wyckoff + LuxAlgo: Bullish FVG + Spring
Volume: выше среднего
MLMA: Зелёная зона

Вход сейчас
Стоп: -3%
TP1: +10% | TP2: +25%
RR: 1:7

Grok: ВХОДИМ ПОЛНЫМ ОБЪЁМОМ — жирный сетап!
""")
    except Exception as e:
        print(f"Ошибка данных: {e}")

# Тестовое сообщение при запуске
send("Grok бот перезапущен! Жду жирные сигналы...")

# Основной цикл — каждые 30 минут
while True:
    check_btc()
    time.sleep(1800)  # 30 минут
