import os
import json
import requests
from datetime import datetime
import time

# Конфигурация
BYBIT_URL = "https://api2.bybit.com/spot/api/launchpool/v1/home"
GATE_URL = "https://www.gate.tv/api/web/v1/financial/launch-pool-get-project-list?page=1&pageSize=18&status=0"
BITGET_URL = "https://www.bitgetapp.com/v1/finance/poolx/product/page/list/new"
HEADERS_BYBIT = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}
SAVE_PATH = "./pools_data"

# Функция получения данных с бирж
def fetch_pools():
    os.makedirs(SAVE_PATH, exist_ok=True)
    pools_data = {}

    # Bybit
    try:
        print("Fetching Bybit pools...")
        response = requests.get(BYBIT_URL, headers=HEADERS_BYBIT)
        response.raise_for_status()
        bybit_data = response.json()
        pools_data["bybit"] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pools": bybit_data.get("result", {}).get("list", []),
        }
        with open(os.path.join(SAVE_PATH, "bybit_pools.json"), "w") as file:
            json.dump(pools_data["bybit"], file, indent=4)
        print("Bybit pools saved.")
    except Exception as e:
        print(f"Failed to fetch Bybit pools: {e}")

    # Gate
    try:
        print("Fetching Gate pools...")
        response = requests.get(GATE_URL)
        response.raise_for_status()
        gate_data = response.json()
        pools_data["gate"] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pools": gate_data.get("data", {}).get("list", []),
        }
        with open(os.path.join(SAVE_PATH, "gate_pools.json"), "w") as file:
            json.dump(pools_data["gate"], file, indent=4)
        print("Gate pools saved.")
    except Exception as e:
        print(f"Failed to fetch Gate pools: {e}")

    # Bitget
    try:
        print("Fetching Bitget pools...")
        payload = {"myProjects": False, "status": 0, "pageSize": 900, "pre": False}
        response = requests.post(BITGET_URL, json=payload)
        response.raise_for_status()
        bitget_data = response.json()
        pools_data["bitget"] = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pools": bitget_data.get("data", {}).get("items", []),
        }
        with open(os.path.join(SAVE_PATH, "bitget_pools.json"), "w") as file:
            json.dump(pools_data["bitget"], file, indent=4)
        print("Bitget pools saved.")
    except Exception as e:
        print(f"Failed to fetch Bitget pools: {e}")

if __name__ == "__main__":
    while True:
        print("Starting fetch process...")
        fetch_pools()
        print("Fetch process complete. Waiting for the next hour...")
        time.sleep(3600)
