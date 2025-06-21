from aiogram import Bot, Dispatcher, types
from aiogram.client.session import aiohttp
from aiogram.fsm.state import StatesGroup, State
from settings import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


class AuthStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        "👋 Привет! Я бот для авторизации на сайте.\n\n"
        "🔹 /register – Зарегистрироваться\n"
        "🔹 /login – Войти"
    )

@dp.message_handler(commands=['register'])
async def register(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.URL_HOME_SERVICE}/register",
            json={"telegram_id": message.from_user.id, "username": message.from_user.username}
        ) as resp:
            if resp.status == 200:
                await message.reply("✅ Вы зарегистрированы!")
            else:
                await message.reply("❌ Ошибка регистрации")

@dp.message_handler(commands=['login'])
async def login(message: types.Message):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{settings.URL_HOME_SERVICE}/token",
            data={"telegram_id": message.from_user.id}
        ) as resp:
            if resp.status == 200:
                token_data = await resp.json()
                await message.reply(f"🔑 Ваш токен: `{token_data['access_token']}`", parse_mode="Markdown")
            else:
                await message.reply("❌ Ошибка входа")
