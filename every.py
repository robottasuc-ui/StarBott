import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from supabase import create_client, Client

# ======================================================
# 1. ТОКЕН АДМИН-БОТА (в который ты будешь кидать фото)
# ======================================================
ADMIN_BOT_TOKEN = '8270591413:AAEaFHugdFoIP-hJKoNbBE8LBaJxb0-MGtQ'

# ======================================================
# 2. ТОКЕН ИГРОВОГО БОТА (от имени которого уйдет рассылка)
# ======================================================
GAME_BOT_TOKEN = '8451029637:AAHF6jJdQ98QhYRRsJxH_wuktMeE5QctT-I'

# Твой ID (чтобы никто другой не мог командовать рассылкой)
ADMIN_ID = 8015661230 

# Данные Supabase
SUPABASE_URL = 'https://mwsbkpfarhdankpyifbm.supabase.co'
SUPABASE_KEY = 'sb_publishable_Bj40x3HKomgXSyLMiVqXig_FqCgOSmA'

# Инициализируем обоих ботов
admin_bot = Bot(token=ADMIN_BOT_TOKEN)
game_bot = Bot(token=GAME_BOT_TOKEN)
dp = Dispatcher()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@dp.message(F.photo, lambda m: m.from_user.id == ADMIN_ID)
async def handle_broadcast(message: Message):
    # 1. Получаем список ID всех игроков из базы
    try:
        res = supabase.table("users").select("user_id").execute()
        users = res.data
    except Exception as e:
        await message.answer(f"Ошибка базы: {e}")
        return

    await message.answer(f"🚀 Начинаю рассылку через игрового бота на {len(users)} чел...")

    done = 0
    blocked = 0
    
    # Берем самое лучшее качество фото
    photo_id = message.photo[-1].file_id
    caption = message.caption or ""

    # 2. Рассылаем через ИГРОВОГО БОТА
    for u in users:
        try:
            user_id = u['user_id']
            # Используем game_bot для отправки!
            await game_bot.send_photo(chat_id=user_id, photo=photo_id, caption=caption)
            done += 1
            await asyncio.sleep(0.05) # Защита от бана за спам
        except:
            blocked += 1

    await message.answer(f"✅ Готово!\nДоставлено: {done}\nЮзеров заблокали бота: {blocked}")

async def main():
    # Слушаем только админ-бота
    await dp.start_polling(admin_bot)

if __name__ == "__main__":
    asyncio.run(main())
