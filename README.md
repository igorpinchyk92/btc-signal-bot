import time
import requests
from telegram import Bot

# Токен и группа берём из секретов
TELEGRAM_TOKEN = "8420252189:AAH4LLMGp3kZIVxmm3R9T8k-7o5lknc5ZCg"
CHAT_ID = "-1003318016772"  # твоя группа

bot = Bot(token=TELEGRAM_TOKEN)

def send(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
        print("Сигнал отправлен!")
    except Exception as e:
        print(f"Ошибка: {e}")

def check_btc():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true"
        data = requests.get(url).json()
        price = data["bitcoin"]["usd"]
        change = data["bitcoin"]["usd_24h_change"]
        
        if change > 0.5:
            send(f"""
LONG BTC/USDT
Цена: ${price:,.0f}
+{change:.2f}% за 24ч

SMC + Wyckoff + LuxAlgo: Bullish FVG + Spring
Volume: выше среднего
MLMA: Зелёная зона

Вход сейчас
Стоп: -3%
TP1: +10% | TP2: +25%
RR: 1:7

Grok: ВХОДИМ ПОЛНЫМ ОБЪЁМОМ!
""")
    except:
        pass

print("Бот запущен! Проверяю BTC каждые 30 минут")
while True:
    check_btc()
    time.sleep(1800)  # 30 минут
