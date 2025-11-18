import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor

TOKEN = "8562737383:AAHRw7WB0n10Qnmrak8_dKYK5tc1Y_uN8gg"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Оживить одно фото — 100 ₽", callback_data="pay_one"))
    kb.add(InlineKeyboardButton("Оживить несколько фото — 250 ₽", callback_data="pay_multi"))
    await message.answer(
        "Привет! 👋\nЯ оживляю фотографии с помощью AI. Выберите пакет:",
        reply_markup=kb
    )

@dp.callback_query_handler(lambda c: c.data.startswith("pay_"))
async def payment_handler(callback: types.CallbackQuery):
    price = 100 if callback.data == "pay_one" else 250
    await bot.send_message(
        callback.from_user.id,
        f"Стоимость услуги: {price} ₽.\nОплата пока через заглушку — просто нажмите 'Готово', когда якобы оплатили.",
        reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton("Готово", callback_data="paid")
        )
    )

@dp.callback_query_handler(lambda c: c.data == "paid")
async def confirm_payment(callback: types.CallbackQuery):
    await bot.send_message(callback.from_user.id, "Отлично! Отправьте фото, которое хотите оживить.")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):
    await message.answer("Обрабатываю фото... Подождите 5–10 секунд ⏳")
    file_id = message.photo[-1].file_id
    await message.answer_photo(file_id, caption="Ваше оживлённое фото готово! 🎉 (пока заглушка)")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
