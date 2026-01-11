osna-biz-startup/
├── app/                # Веб-адмінка (Flask)
│   ├── static/
│   ├── templates/
│   └── routes.py
├── bot/                # Telegram Бот (aiogram)
│   ├── handlers/       # Логіка команд
│   ├── keyboards/      # Кнопки
│   └── main.py         # Точка входу бота
├── core/               # Спільний код (БД, логіка, сервіси)
│   ├── database.py     # SQLAlchemy / Tortoise
│   ├── models.py       # Ті самі таблиці БД
│   └── config.py       # Налаштування з .env
├── migrations/         # Alembic (контроль версій БД)
├── .env                # Твої секрети (в .gitignore!)
├── requirements.txt
├── docker-compose.yml  # Для бази та майбутнього продакшену
└── README.md
