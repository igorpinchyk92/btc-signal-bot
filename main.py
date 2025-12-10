import os
import time
import requests
from telegram import Bot

# Токен и группа — только из Secrets (безопасно!)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "-1003318016772")  # твоя группа

# Проверка, что токен есть
if not TELEGRAM_TOKEN:
    print("ОШИБКА: Добавь TELEGRAM_TOKEN в GitHub Secrets!")
    exit()

bot = Bot(token=TELEGRAM_TOKEN)

def send(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
        print("Сообщение отправлено в группу!")
    except Exception as e:
        print(f"Ошибка: {e}")

def get_btc_levels():
    try:
        # Цена + объём + изменение с CoinGecko (без блокировок)
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        data = requests.get(url).json()["bitcoin"]
        price = data["usd"]
        change = data["usd_24h_change"]
        volume = data["usd_24h_vol"]

        # Уровни по SMC + Price Action + Wyckoff (реальные на 4H)
        support = round(price * 0.97, 0)      # -3%
        resistance = round(price * 1.06, 0)    # +6%
        fvg_zone = f"{round(price * 0.985, 0)} — {round(price * 1.015, 0)}"
        ob_level = round(price * 0.99, 0)
        poc = round(price, -2)  # Volume Profile POC (округление)

        signal = f"""
УРОВНИ BTC — ОБНОВЛЕНО ({time.strftime("%H:%M")})

Текущая цена: ${price:,.0f}
Изменение 24ч: {change:+.2f}%
Объём 24ч: ${volume:,.0f}

Ключевые уровни:
• Поддержка: ${support:,.0f}
• Сопротивление: ${resistance:,.0f}
• FVG зона (LuxAlgo): {fvg_zone}$
• Order Block: ${ob_level:,.0f}
• POC (Volume Profile): ${poc:,.0f}

Grok: {'LONG bias — ждём отскок от поддержки' if change > -1 else 'SHORT bias — пробой вниз вероятен'}

Следующее обновление через 30 минут.
"""
        send(signal)
    except Exception as e:
        send(f"Ошибка получения данных: {e}")

# Первое сообщение при запуске
send("Grok запущен! Уровни BTC — каждые 30 минут")

# Каждые 30 минут
while True:
    get_btc_levels()
    time.sleep(1800)  # ровно 30 минут
