import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject

# НОВЫЙ ТОКЕН ДЛЯ АВТОРИЗАЦИИ
TOKEN = "8511507570:AAFdh93-EBWLe7LGKSPHtcgEkI_opfH6tn0"
SB_URL = "https://mwsbkpfarhdankpyifbm.supabase.co"
SB_KEY = "sb_publishable_Bj40x3HKomgXSyLMiVqXig_FqCgOSmA"

headers = {
    "apikey": SB_KEY,
    "Authorization": f"Bearer {SB_KEY}",
    "Content-Type": "application/json"
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def auth_handler(message: types.Message, command: CommandObject):
    user_id = message.from_user.id
    args = command.args # Это будет auth_xxxxx из ссылки на сайте

    if args and args.startswith("auth_"):
        try:
            # Обновляем auth_status, чтобы сайт увидел вход
            res = requests.patch(
                f"{SB_URL}/rest/v1/users?user_id=eq.{user_id}", 
                headers=headers, 
                json={"auth_status": args} 
            )
            if res.status_code in [200, 204]:
                await message.answer("✅ **Вход подтвержден!**\nТеперь вернись на сайт.")
            else:
                await message.answer("❌ Ошибка: Сначала нажми /start в основном боте игры!")
        except:
            await message.answer("⚠️ Ошибка базы данных.")
    else:
        await message.answer("👋 Этот бот только для подтверждения входа.")

# Таймер для GitHub Actions (5 часов 50 минут)
async def shutdown_timer():
    await asyncio.sleep(21000)
    os._exit(0)

async def main():
    print("Auth Bot запущен...")
    asyncio.create_task(shutdown_timer())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
