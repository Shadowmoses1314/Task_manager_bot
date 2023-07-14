# Telegram Manager Bot

Это простой Telegram-бот для управления задачами. Менеджер может отправлять задания сотрудникам, а сотрудники могут выбрать один из вариантов ответа.

## Установка

1. Клонируйте репозиторий:

```shell
git clone https://github.com/Shadowmoses1314/Task_manager_bot.git
```

2. Перейдите в директорию проекта:

```shell
cd telegram_manager_bot
```

3. Установите зависимости:

```shell
python -m venv env
source env/Scripts/activate
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

4. Создайте файл `.env` и добавьте необходимые переменные окружения:

```plaintext
TELEGRAM_TOKEN=your-telegram-bot-token
MANAGER_CHAT_ID=your-manager-chat-id
```

## Использование

1. Запустите бота:

```shell
python main.py
```

2. В Telegram найдите вашего бота и нажмите кнопку "Старт".
