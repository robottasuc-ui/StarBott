import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import WebAppInfo

# --- ТВОИ ДАННЫЕ (НЕ УДАЛЕНО) ---
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

# --- ТВОЯ ЛОГИКА (НЕ УДАЛЕНО) ---
@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    username = message.from_user.username or "Gamer"
    args = command.args

    if args and args.startswith("auth_"):
        try:
            res = requests.patch(f"{SB_URL}/rest/v1/users?user_id=eq.{user_id}", 
                                 headers=headers, json={"auth_status": "verified"})
            await message.answer("✅ Авторизация успешна!")
        except: pass
        return

    try:
        check_user = requests.get(f"{SB_URL}/rest/v1/users?user_id=eq.{user_id}", headers=headers).json()
        if not check_user:
            new_user = {"user_id": user_id, "username": username, "stars": 0, "balance": 0.0, "inventory": [], "tickets": 0}
            requests.post(f"{SB_URL}/rest/v1/users", headers=headers, json=new_user)
    except: pass

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="🚀 Запустить StarDrop", web_app=WebAppInfo(url=WEB_APP_URL)))
    builder.row(types.InlineKeyboardButton(text="🌐 Перейти на сайт", url=SITE_URL))
    
    await message.answer_photo(photo=WELCOME_PHOTO_URL, caption=f"👋 Привет, {username}!", reply_markup=builder.as_markup())

# --- ФИКС ДЛЯ РАБОТЫ 24/7 ЧЕРЕЗ GITHUB ACTIONS ---
async def shutdown_timer():
    """Таймер, который выключит бота через 5 часов 50 минут для мягкого перезапуска GitHub"""
    await asyncio.sleep(21000) 
    print("Плановая перезагрузка сессии...")
    os._exit(0)

async def main():
    print("Бот запущен и готов к работе!")
    # Запускаем фоновый таймер
    asyncio.create_task(shutdown_timer())
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
