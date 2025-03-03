# 🚀 Crypto Pools Bot & Data Scraper

Этот проект включает в себя **два основных скрипта**:

1. **[`stabletable.py`](./stabletable.py)** – Парсер данных о пулах с бирж **Bybit, Gate.io и Bitget**.
2. **[`bot.py`](./bot.py)** – Телеграм-бот для отображения актуальных пулов.

## 📌 Функционал

✅ Автоматический сбор данных о пулах **каждый час**  
✅ Вывод актуальных пулов в **Telegram**  
✅ Поддержка **Bybit, Gate.io, Bitget**  
✅ **Фильтрация пулов**: убираются завершённые пулы  
✅ **Обновление по команде**: можно вручную обновить список  

## 🛠 Установка и запуск

### 🔹 1. Клонирование репозитория

```bash
git clone https://github.com/yourusername/cryptools.git
cd cryptools
```

### 🔹 2. Установка виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\\Scripts\\activate  # (Windows)
```

### 🔹 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 🔹 4. Настройка Telegram-бота
Создайте файл `token.txt` и вставьте туда **токен** вашего бота.

```bash
echo "YOUR_TELEGRAM_BOT_TOKEN" > token.txt
```

### 🔹 5. Запуск парсера (раз в час)
Добавьте в `crontab` (Linux) или настройте `Task Scheduler` (Windows):

```bash
0 * * * * /path/to/venv/bin/python3 /path/to/stabletable.py
```

**Или запустите вручную:**
```bash
python3 stabletable.py
```

### 🔹 6. Запуск бота на постоянку
Используйте `nohup`, чтобы бот работал в фоновом режиме:

```bash
nohup python3 bot.py > bot.log 2>&1 &
```

📄 **Проверить логи бота:**
```bash
tail -f bot.log
```

🛑 **Остановить бота:**
```bash
pkill -f bot.py
```

## 🔧 TODO (План доработок)
- [ ] Web-интерфейс для мониторинга пулов  
- [ ] Выделение списка данных отдельно для **FinKeeper**  
- [ ] Добавление кликабельной информации про пулы в боте  
- [ ] Улучшенный формат вывода для удобного восприятия  

---

✉️ **Связь**: Если есть предложения или баги — пишите в Issues! 🚀
