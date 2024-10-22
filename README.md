# Простой Telegram бот на aiogram

```
Этот проект демонстрирует создание простого Telegram бота на фреймворке aiogram 3.7.0 с интеграцией базы данных 
PostgreSQL.

Суть проекта - демонстрация того, как использовать LLama3 бесплатно, без ограничений и без запуска модели на своем 
компьютере или сервере.

В данном примере я использовал мощности сервиса groq.com. Там получил бесплатный апи ключ и уже с его помощью развернул 
языковую модель "llama3-70b-8192".

На своем Хабре выпущу подробное описание данного кода.

```

## Установка

где requirements.txt содержит следующие зависимости:

``` requirements
asyncpg-lite~=0.3.1.3
aiogram~=3.7.0
python-decouple
groq
pytz
```

Создайте файл .env в корне проекта и добавьте в него следующие переменные:

``` textmate

GROQ_API_KEY=your_groq_token
BOT_API_KEY=your_bot_token
ADMINS=admin1,admin2
ROOT_PASS=your_root_password
PG_LINK=postgresql://username:password@host:port/dbname

``` 

Замените данные на свои. Предварительно не забудьте узнать свой телеграмм ID, развернуть базу данных и создать токен
бота и токен GROQ_API.

## Запустите бота:

``` bash
python aiogram_run.py
``` 

## Структура проекта

```markdown
- db_handler
    - __init__.py: Инициализация модуля.
    - db_funk.py: Функции для взаимодействия с PostgreSQL.

- handlers
    - __init__.py: Инициализация модуля.
    - user_router.py: Основной и единственный роутер в котором весь код

- keyboards
    - __init__.py: Инициализация модуля.
    - kbs.py: Файл со всеми клавиатурами.

- utils
    - __init__.py: Инициализация модуля.
    - utils.py: Файл с утилитами.
```

### Корневые файлы проекта

```markdown
- .env
- .dockerignorefile
- Dockerfile
- Makefile: файл для удобного запуска и управления контейнерами
- .gitignorefile
- aiogram_run.py: файл для запуска бота
- create_bot.py: файл с настройками бота
- llama_groq_demo.py: демка LLama3с работой через GROQ
- llama_localhost_demo.py: демка LLama3с с локальным запуском
- README.md: Короткое описание проекта с GitHub
```

# Лицензия

Этот проект лицензирован под MIT License.