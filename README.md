# ITMO AI / AI Product Bot (aiogram v3)

Телеграм-бот, который помогает абитуриентам разобраться с магистратурами **AI** и **AI Product** в ИТМО:
- показывает **обязательные** и **элективные** дисциплины по семестрам,
- отвечает на **FAQ** (срок, форма обучения, разница программ),
- делает **рекомендации по элективам** по интересам (NLP, CV, ML, Product),
- умеет **поиск по курсам** и **избранное**.

## Стек
- Python 3.10+
- aiogram v3
- JSON (источник учебных планов)

## Структура
itmo_bot/
├─ bot/
│ └─ app.py
├─ core/
│ ├─ loader.py
│ ├─ faq.py
│ ├─ recommender.py
│ ├─ relevancy.py
│ └─ init.py
├─ data/
│ ├─ ai.json
│ ├─ ai_product.json
│ └─ favorites.json # создастся автоматически
└─ requirements.txt
## Установка и запуск

1) Установить зависимости:
```bash
pip install -r requirements.txt
Получить токен у @BotFather → TG_TOKEN.

Передать токен боту через переменные окружения:

Windows (PowerShell):

powershell
Копировать
Редактировать
setx TG_TOKEN "1234567890:ABC..."
Linux/macOS (bash/zsh):


export TG_TOKEN="1234567890:ABC..."
В PyCharm: Run → Edit Configurations → Environment variables → TG_TOKEN=....

Запуск:


python bot/app.py
Примеры команд
/programs — список программ

/semester 1 AI — курсы семестра

/semester 2 "AI Product" — курсы семестра

/search nlp — поиск по названию

/interests nlp, cv — рекомендации

/favorites — показать избранное

/fav_add Полное название курса — добавить

/fav_clear — очистить избранное

Данные
Файлы data/ai.json и data/ai_product.json должны иметь формат:

json

{
  "program": "AI",
  "semesters": [
    {
      "num": 1,
      "mandatory": ["Математический анализ"],
      "electives": ["Введение в NLP"]
    }
  ]
}
Безопасность токена
Не коммитьте TG_TOKEN в репозиторий.

Храните в переменных окружения или в .env (и внесите .env в .gitignore).

Лицензия
MIT (при желании поменяйте).

yaml


---

# .gitignore (положи в корень проекта)

```gitignore
# виртуальные окружения
.venv/
venv/
env/

# кэш и артефакты
__pycache__/
*.pyc
*.pyo
*.pyd
*.log

# IDE
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db

# токены и локальные конфиги
.env
data/favorites.json

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# ITMO Telegram Bot

This is a simple Telegram bot built with **Python** and the **Aiogram 2.x** framework.  
The bot can respond to commands and messages, providing basic interaction with users.

---

## Features
- `/start` — Sends a greeting message.
- `/help` — Displays available commands.
- Text messages — Replies with a default response.
- Easy to expand with new commands and handlers.

---

## Requirements
- Python 3.9+
- [Aiogram 2.25.1](https://docs.aiogram.dev/en/latest/)
- Other dependencies listed in `requirements.txt`

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/itmo-bot.git
   cd itmo-bot
Create and activate a virtual environment:


python -m venv .venv
source .venv/bin/activate   # On Linux/Mac
.venv\Scripts\activate      # On Windows
Install dependencies:



pip install -r requirements.txt
Create a .env file in the project root and add your Telegram bot token:


TG_TOKEN=your_telegram_token_here
Running the bot
Start the bot with:

python bot/app.py
Project structure
bash

itmo-bot/
│── bot/
│   ├── app.py          # Main bot logic
│   ├── __init__.py     # Initialization
│── .env                # Environment variables (not pushed to GitHub)
│── requirements.txt    # Dependencies
│── README.md           # Project description
Deployment
You can deploy the bot on:

Heroku

PythonAnywhere

Docker container

Or any server with Python 3.9+

License
This project is for educational purposes at ITMO University.
Feel free to use and modify for your own learning.
