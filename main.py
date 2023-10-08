from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from bot import user_interaction, states
import config
from models.postgres_storage import PostgresStorage

# Создание экземпляра бота и передача хранилища PostgresStorage в диспетчер.
bot = Bot(token=config.TOKEN)
storage = PostgresStorage(f'dbname={config.DB_NAME} user={config.DB_USER} password={config.DB_PASS} host={config.DB_HOST}')

dp = Dispatcher(bot, storage=storage)  # Предполагаем, что DSN находится в config
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    await user_interaction.process_start_command(message, state)

@dp.message_handler(lambda message: message.text, state=states.UserState.ENTER_NAME)
async def user_entering_name(message: types.Message, state: FSMContext):
    await user_interaction.process_enter_name(message, state)

@dp.message_handler(lambda message: message.text, state=states.UserState.CHOOSE_FILE)
async def user_choosing_file(message: types.Message, state: FSMContext):
    await user_interaction.process_choose_file(message, state)

@dp.message_handler(lambda message: message.text, state=states.UserState.CHOOSE_DELIVERY)
async def user_choosing_delivery(message: types.Message, state: FSMContext):
    await user_interaction.process_choose_delivery(message, state)

@dp.message_handler(lambda message: message.text, state=states.UserState.ASKING_EMAIL)
async def user_choosing_delivery(message: types.Message, state: FSMContext):
    await user_interaction.process_email(message, state)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('file:'))
async def process_file_chosen(callback_query: CallbackQuery, state: FSMContext):
    _, file_id = callback_query.data.split(":")

    # Здесь ваш код для обработки выбора файла

    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
