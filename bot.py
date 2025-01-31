import asyncio
import json
import os
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

# Читаем токен из файла token.txt
with open("token.txt", "r") as file:
    TOKEN = file.read().strip()

# Инициализируем бота и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()

# Функция загрузки JSON-файлов
def load_json(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

# Функция форматирования оставшегося времени
def format_time_left(end_timestamp):
    now = datetime.utcnow().timestamp()
    remaining_time = end_timestamp - now
    if remaining_time <= 0:
        return None  # Пропускаем завершенные пулы
    days = int(remaining_time // 86400)
    hours = int((remaining_time % 86400) // 3600)
    return f"{days}d {hours}h"

# Функция вычисления времени обновления пулов
def format_time_since(timestamp_str):
    try:
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        now = datetime.utcnow().replace(tzinfo=timezone.utc)
        delta = now - timestamp
        minutes_ago = int(delta.total_seconds() // 60)
        return "только что" if minutes_ago < 1 else f"{minutes_ago} мин назад"
    except ValueError:
        return "неизвестно"

# Обработчик команды /start и /pools
@dp.message(Command("start", "pools"))
async def send_pools(message: Message):
    bybit_data = load_json("pools_data/bybit_pools.json")
    gate_data = load_json("pools_data/gate_pools.json")
    bitget_data = load_json("pools_data/bitget_pools.json")

    response = "📊 **Актуальные пулы:**\n\n"

    # Gate.io
    if gate_data and "pools" in gate_data:
        updated_time = format_time_since(gate_data["timestamp"])
        response += f"✅ **Gate** *(Обновлено: {updated_time})*\n"

        reward_dict = {}
        for project in gate_data["pools"]:
            reward_coin = project["coin"]
            time_left = format_time_left(project["end_timest"])

            if time_left is None:
                continue  # Пропускаем завершенные пулы

            staking_list = []
            for pool in project["reward_pools"]:
                staking_coin = pool["coin"]
                apr = float(pool["rate_year"])
                is_new_user_pool = pool.get("limit_rule") == 1
                new_user_emoji = " 🆕👤" if is_new_user_pool else ""
                emoji = "💲" if staking_coin == "USDT" else "🔹"
                staking_list.append(f"{emoji} {staking_coin} ({apr:.2f}% APR){new_user_emoji}")

            reward_dict[reward_coin] = {
                "time_left": time_left,
                "staking_list": staking_list
            }

        if not reward_dict:
            response += "Нет активных пулов\n\n"
        else:
            for reward_coin, pool_data in reward_dict.items():
                response += f"**{reward_coin}** - {pool_data['time_left']}\n"
                for staking_info in pool_data["staking_list"]:
                    response += f"{staking_info}\n"
                response += "\n"
    else:
        response += "❌ Gate: Ошибка загрузки данных\n\n"

    # Bybit
    if bybit_data and "pools" in bybit_data:
        updated_time = format_time_since(bybit_data["timestamp"])
        response += f"✅ **Bybit** *(Обновлено: {updated_time})*\n"
        if not bybit_data["pools"]:
            response += "Нет активных пулов\n\n"
        else:
            for pool in bybit_data["pools"]:
                pool_name = pool["returnCoin"]
                time_left = format_time_left(pool["stakeEndTime"] / 1000)
                for stake in pool["stakePoolList"]:
                    apr = float(stake["apr"])
                    coin = stake["stakeCoin"]
                    usdt_emoji = "💲" if coin == "USDT" else "🔹"
                    response += f"{usdt_emoji} {pool_name} ({coin}) - {apr:.2f}% APR, ends in {time_left}\n"
            response += "\n"
    else:
        response += "❌ Bybit: Ошибка загрузки данных\n\n"

    # Bitget
    if bitget_data and "pools" in bitget_data:
        updated_time = format_time_since(bitget_data["timestamp"])
        response += f"✅ **Bitget** *(Обновлено: {updated_time})*\n"
        if not bitget_data["pools"]:
            response += "Нет активных пулов\n\n"
        else:
            for pool in bitget_data["pools"]:
                pool_name = pool["productCoinName"]
                time_left = format_time_left(pool["endTime"] / 1000)
                for stake in pool["productSubList"]:
                    apr = float(stake["apr"])
                    coin = stake["productSubCoinName"]
                    usdt_emoji = "💲" if coin == "USDT" else "🔹"
                    if time_left:
                        response += f"{usdt_emoji} {pool_name} ({coin}) - {apr:.2f}% APR, ends in {time_left}\n"
            response += "\n"
    else:
        response += "❌ Bitget: Ошибка загрузки данных\n\n"

    response += "🔄 Чтобы получить данные о пулах, нажмите /pools (данные обновляются раз в час)"

    await message.answer(response, disable_web_page_preview=True)

# Запуск бота
async def main():
    print("✅ Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
