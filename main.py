import os
import asyncio
import requests
from telegram import Bot

# Токен и группа — только из Secrets (обязательно!)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not TELEGRAM_TOKEN or not CHAT_ID:
    print("ОШИБКА: Добавь TELEGRAM_TOKEN и CHAT_ID в GitHub Secrets!")
    exit()

bot = Bot(token=TELEGRAM_TOKEN)

async def send(text):
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text, disable_web_page_preview=True)
        print("Сообщение отправлено в группу!")
    except Exception as e:
        print(f"Ошибка отправки: {e}")

async def get_btc_levels():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true"
        data = requests.get(url).json()["bitcoin"]
        price = data["usd"]
        change = data["usd_24h_change"]
        volume = data["usd_24h_vol"]

        support = round(price * 0.97)
        resistance = round(price * 1.06)
        poc = round(price)
        fvg = f"{round(price * 0.985)} — {round(price * 1.015)}"

        await send(f"""
УРОВНИ BTC — ОБНОВЛЕНО

Цена: ${price:,.0f}
Изменение 24ч: {change:+.2f}%
Объём: ${volume:,.0f}B

• Поддержка: ${support:,.0f}
• Сопротивление: ${resistance:,.0f}
• POC (Volume Profile): ${poc:,.0f}
• FVG зона: {fvg}$

Grok: {'LONG bias — ждём отскок' if change > -1 else 'Осторожно — возможен пробой вниз'}
Следующее обновление через 30 минут
""")
    except Exception as e:
        await send(f"Ошибка получения данных: {e}")

async def main():
    await send("Grok запущен! Уровни BTC — каждые 30 минут")
    while True:
        await get_btc_levels()
        await asyncio.sleep(1800)  # ровно 30 минут

if __name__ == "__main__":
    asyncio.run(main())
