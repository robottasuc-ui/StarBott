import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8451029637:AAHF6jJdQ98QhYRRsJxH_wuktMeE5QctT-I"
SB_URL = "https://mwsbkpfarhdankpyifbm.supabase.co"
SB_KEY = "sb_publishable_Bj40x3HKomgXSyLMiVqXig_FqCgOSmA"

headers = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=minimal"
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

WELCOME_PHOTO_URL = "https://i.postimg.cc/G3S5cMJS/logo.jpg"
WEB_APP_URL = "https://stars-drop.vercel.app"
SITE_URL = "https://stars-drop-site.vercel.app/"

# --- ЛОГИКА ПРИВЕТСТВИЯ ---
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username or "Gamer"

    # Регистрация пользователя в базе
    try:
        check_res = requests.get(f"{SB_URL}/rest/v1/users?user_id=eq.{user_id}", headers=headers)
        if check_res.status_code == 200 and not check_res.json():
            new_user = {
                "user_id": user_id, 
                "username": username, 
                "stars": 0, 
                "balance": 0.0, 
                "inventory": [], 
                "tickets": 0
            }
            requests.post(f"{SB_URL}/rest/v1/users", headers=headers, json=new_user)
    except Exception as e:
        print(f"Ошибка базы: {e}")

    # 1. Кнопка ПОД картинкой (только ссылка на сайт)
    inline_builder = InlineKeyboardBuilder()
    inline_builder.row(types.InlineKeyboardButton(text="🌐 Перейти на сайт", url=SITE_URL))
    
    # 2. Большая кнопка СНИЗУ (Menu Button / Reply Keyboard)
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.row(types.KeyboardButton(
        text="🎮 Играть", 
        web_app=WebAppInfo(url=WEB_APP_URL)
    ))

    # Отправка сообщения
    await message.answer_photo(
        photo=WELCOME_PHOTO_URL, 
        caption=(
            f"👋 Привет, {username}!\n\n"
            "Добро пожаловать на **StarsDrop**.\n\n"
            "📍 Выбирай удобный способ игры:\n"
            "— Переходи на наш полноценный **сайт** по кнопке ниже.\n"
            "— Или нажимай синюю кнопку **«Играть»** в меню бота!"
        ),
        parse_mode="Markdown",
        reply_markup=inline_builder.as_markup()
    )
    
    # Отправляем клавиатуру с нижней кнопкой отдельным сообщением (или обновляем интерфейс)
    await message.answer("Удачи в игре! 👇", reply_markup=reply_builder.as_markup(resize_keyboard=True))

# --- СИСТЕМА 24/7 ---
async def shutdown_timer():
    await asyncio.sleep(21000) 
    os._exit(0)

async def main():
    print("Основной бот запущен!")
    asyncio.create_task(shutdown_timer())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
