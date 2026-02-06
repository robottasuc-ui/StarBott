import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject

# Используй НОВЫЙ токен от второго бота здесь
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
    args = command.args

    if args and args.startswith("auth_"):
        try:
            res = requests.patch(
                f"{SB_URL}/rest/v1/users?user_id=eq.{user_id}", 
                headers=headers, 
                json={"auth_status": "verified"}
            )
            if res.status_code in [200, 204]:
                await message.answer("✅ **Вход подтвержден!**\n\nТеперь вернитесь на сайт, страница обновится.")
            else:
                await message.answer("❌ Ошибка базы данных.")
        except:
            await message.answer("⚠️ Ошибка соединения.")
    else:
        await message.answer("👋 Этот бот только для подтверждения входа через сайт.")

async def main():
    print("Бот АВТОРИЗАЦИИ запущен...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
