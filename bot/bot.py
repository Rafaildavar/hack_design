import os
import asyncio
from enum import Enum
from typing import Dict, Optional

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
import httpx


# Загружаем переменные окружения
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не указан в .env")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class AuthState(str, Enum):
    NONE = "none"
    WAITING_LOGIN = "waiting_login"
    WAITING_PASSWORD = "waiting_password"
    AUTHORIZED = "authorized"


# Состояния и связки пользователей
user_states: Dict[int, AuthState] = {}          # telegram_id -> состояние авторизации
user_temp_login: Dict[int, str] = {}            # временно храним логин до ввода пароля
linked_users: Dict[int, int] = {}               # telegram_id -> user_id из БД бэка


async def auth_with_backend(login: str, password: str, telegram_id: int) -> Optional[int]:
    """
    Отправляет логин/пароль/telegram_id на бэк.
    Ожидает, что бэк вернёт JSON:
      { "success": true, "user_id": 42 }  либо { "success": false, "error": "..." }

    Возвращает user_id при успехе, иначе None.
    """
    url = f"{BACKEND_URL}/api/auth/telegram-login"
    payload = {
        "login": login,
        "password": password,
        "telegram_id": telegram_id,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    if data.get("success"):
        return data.get("user_id")
    else:
        # Можно залогировать data.get("error")
        return None


@dp.message(CommandStart())
async def cmd_start(message: Message):
    telegram_id = message.from_user.id

    # Уже привязан к аккаунту
    if telegram_id in linked_users:
        user_id = linked_users[telegram_id]
        user_states[telegram_id] = AuthState.AUTHORIZED
        await message.answer(
            f"Снова привет! ✅\n"
            f"Твой аккаунт уже связан (user_id={user_id}).\n\n"
            f"Можешь сразу писать свои вопросы по учёбе."
        )
        return

    # Начинаем процесс авторизации
    user_states[telegram_id] = AuthState.WAITING_LOGIN
    await message.answer(
        "Привет! 👋\n"
        "Это ИИ-ассистент студента.\n\n"
        "Для начала давай привяжем твой аккаунт.\n"
        "Напиши, пожалуйста, *логин* от своей учётки.",
        parse_mode="Markdown"
    )


@dp.message(F.text)
async def handle_text(message: Message):
    telegram_id = message.from_user.id
    text = message.text.strip()
    state = user_states.get(telegram_id, AuthState.NONE)

    # 1) Ждём логин
    if state == AuthState.WAITING_LOGIN:
        user_temp_login[telegram_id] = text
        user_states[telegram_id] = AuthState.WAITING_PASSWORD
        await message.answer(
            "Отлично 👍\n"
            "Теперь введи *пароль* от аккаунта.",
            parse_mode="Markdown"
        )
        return

    # 2) Ждём пароль
    if state == AuthState.WAITING_PASSWORD:
        login = user_temp_login.get(telegram_id)
        password = text

        if not login:
            # На всякий случай, если что-то пошло не так
            user_states[telegram_id] = AuthState.WAITING_LOGIN
            await message.answer(
                "Что-то пошло не так, давай ещё раз.\n"
                "Напиши свой логин."
            )
            return

        await message.answer("Проверяю данные, секунду… 🔑")

        try:
            user_id = await auth_with_backend(login, password, telegram_id)
        except Exception as e:
            # Ошибка при запросе к бэку
            user_states[telegram_id] = AuthState.WAITING_LOGIN
            await message.answer(
                "Не удалось связаться с сервером авторизации 😔\n"
                "Попробуй ещё раз позже или напиши /start."
            )
            print(f"Auth error for {telegram_id}: {e}")
            return

        # Убираем временный логин из памяти
        user_temp_login.pop(telegram_id, None)

        if user_id is None:
            # Логин/пароль неправильные
            user_states[telegram_id] = AuthState.WAITING_LOGIN
            await message.answer(
                "Неверный логин или пароль ❌\n"
                "Попробуй снова: напиши свой логин."
            )
            return

        # Успешная авторизация
        linked_users[telegram_id] = user_id
        user_states[telegram_id] = AuthState.AUTHORIZED

        await message.answer(
            f"Готово, аккаунт привязан ✅\n"
            f"(user_id={user_id}, tg_id={telegram_id})\n\n"
            "Теперь можешь писать учебные вопросы, а я буду отвечать через ИИ-ассистента.\n"
            "Также на этот аккаунт смогут приходить напоминания и другие уведомления."
        )
        return

    # 3) Пользователь не авторизован и не в процессе
    if telegram_id not in linked_users:
        await message.answer(
            "Сначала нужно авторизоваться.\n"
            "Нажми /start и введи логин и пароль."
        )
        return

    # 4) Пользователь уже авторизован — это обычный запрос к ассистенту
    # Здесь просто отправляем текст на бэк (/api/chat)
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            payload = {
                "message": text,
                "history": []  # при желании можно прикрутить историю
            }
            resp = await client.post(f"{BACKEND_URL}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            reply = data.get("reply") or "Сервер не вернул текст ответа :("
    except Exception as e:
        reply = (
            "Ошибка при обращении к бэкенду 😢\n"
            f"`{e}`"
        )

    await message.answer(reply)


async def main():
    print("Telegram-бот запущен…")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
