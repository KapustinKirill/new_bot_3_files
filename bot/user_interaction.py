from aiogram import Bot, types
from aiogram.dispatcher  import FSMContext
from aiogram.dispatcher.filters import Command
from bot import states
from bot.db_interaction import get_user_by_telegram_id, create_user, update_user_state, get_all_files, \
    log_user_file_interaction
from bot.db_interaction import db_session
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from aiogram import Bot, types

import os

from bot.mail import send_email
from models.models import BotFile, BotUser


welcome = """Привет 👋🏻
🤖 Я бот канала PRO Одиночество 
💌 Я умею высылать подарки на электронную почту или прямо в этот чат
Пожалуйста, сообщите мне своё имя для получения подарка 👐🏻"""

chose_file = "Выберите из списка ниже, какой вы хотите получить подарок 👇🏻"
chose_travel = "Выберите куда Вы хотите получить подарок:"
email_send = """Благодарю Вас, 
Скорее проверяйте почту, письмо уже в пути!"""
email_subject = """Материалы от канала PRO Одиночество"""
email_body = """<p>Привет, 
</p>
    <p>В приложении к этому письму находится  твой подарок</p>"""
succses_chat_send = "Вот Ваш подарок:"


def get_full_file_path(file_name):
    # Путь к директории, где находится ваш код
    code_dir_path = os.path.dirname(os.path.abspath(__file__))

    # Путь к корневой директории проекта
    project_root_path = os.path.dirname(code_dir_path)

    # Путь к директории с файлами
    files_dir_path = os.path.join(project_root_path, 'files')

    # Полный путь к файлу
    full_file_path = os.path.join(files_dir_path, file_name)

    return full_file_path


async def send_file_in_chat(file_name: str, message: types.Message):
    """
    Отправляет файл в чат.

    Args:
    file_name (str): Имя файла для отправки.
    message (types.Message): Сообщение от пользователя, полученное ботом.

    """
    # Предположим, что get_file_path(file_name) - это ваша функция, которая возвращает полный путь к файлу.

    file_path = get_full_file_path(file_name)
    print(file_path)
    with open(file_path, 'rb') as file:
        await message.answer_document(file, caption=f"{succses_chat_send}: {file_name}")


async def process_start_command(message: types.Message, state: FSMContext):
    # Проверяем, есть ли пользователь в базе
    with db_session() as db:
        user = get_user_by_telegram_id(message.from_user.id, db)
        if not user:
            # Если нет, переходим в состояние ENTER_NAME
            await states.UserState.ENTER_NAME.set()
            await message.answer(welcome)
        else:
            # Если да, переходим в состояние CHOOSE_FILE
            await states.UserState.CHOOSE_FILE.set()
            await send_file_list(message, state)


async def process_enter_name(message: types.Message, state: FSMContext):
    with db_session() as db:
        # Создаем пользователя в базе и сохраняем его имя
        user_name = message.text
        create_user(telegram_id=message.from_user.id, name=user_name, db=db)

    # Переходим в состояние CHOOSE_FILE и отправляем список файлов
    await states.UserState.CHOOSE_FILE.set()
    await send_file_list(message, state)


async def send_file_list(message: types.Message, state: FSMContext):
    with db_session() as db:
        files = get_all_files(db)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for file in files:
            keyboard.add(types.KeyboardButton(file.name))
        await message.answer(chose_file, reply_markup=keyboard)
        files_data = [file.name for file in files]
        print(f"Saving files data: {files_data}")
        print(state)
        # await state.update_data({"files": files_data})
        await state.update_data({"files": {file.id: file.name for file in files}})

async def process_choose_file(message: types.Message, state: FSMContext):
    # Проверяем, что выбранный файл существует
    user_data = await state.get_data()
    print(user_data, message.text)
    if message.text not in user_data['files'].values():
        await message.answer("Пожалуйста, выберите файл из предложенных.")
        return

    # Сохраняем выбор пользователя и переходим в состояние CHOOSE_DELIVERY
    await state.update_data({"chosen_file": message.text})
    await states.UserState.CHOOSE_DELIVERY.set()

    # Предлагаем варианты доставки файла
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("В чат"))
    keyboard.add(types.KeyboardButton("На почту"))
    await message.answer(chose_travel, reply_markup=keyboard)

async def get_file_name(display_name):
    with db_session() as db:
        file = db.query(BotFile).filter(BotFile.name == display_name).first()
        return file.path if file else None


async def process_choose_delivery(message: types.Message, state: FSMContext):
    # Проверяем валидность выбора
    if message.text not in ["В чат", "На почту"]:
        await message.answer("Пожалуйста, выберите один из предложенных способов доставки.")
        return

    # Сохраняем выбор и логируем взаимодействие пользователя с файлом
    user_data = await state.get_data()
    print(user_data)
    file_id = next((id_ for id_, name in user_data['files'].items() if name == user_data['chosen_file']), None)
    with db_session() as db:
        log_user_file_interaction(user_id=message.from_user.id,
                                  file_id=file_id,
                                  delivery_method=message.text.lower(),
                                  db=db)

    # Отправляем файл по выбранному способу

        # Получаем имя файла из базы данных по его "красивому" имени
        file_name = await get_file_name(user_data['chosen_file'])

        # Проверяем, нашли ли мы файл
        if not file_name:
            await message.answer("Извините, произошла ошибка при поиске файла.")
            return
        # Отправляем файл по выбранному способу
        file_name = await get_file_name(user_data['chosen_file'])
        if not file_name:
            await message.answer("Извините, произошла ошибка при поиске файла.")
            return

        if message.text == "В чат":
            await send_file_in_chat(file_name, message)
            # Переходим обратно в состояние CHOOSE_FILE
            await states.UserState.CHOOSE_FILE.set()
            await send_file_list(message, state)

        elif message.text == "На почту":
            await states.UserState.ASKING_EMAIL.set()
            await message.answer("Пожалуйста, введите ваш адрес электронной почты:")


async def process_email(message: types.Message, state: FSMContext):
    email_address = message.text
    user_data = await state.get_data()

    # Сохраняем адрес электронной почты в базе данных (если нужно)
    with db_session() as db:
        user = db.query(BotUser).filter(BotUser.telegram_id == message.from_user.id).first()
        if user:
            user.email_address = email_address

    # Отправляем файл на указанный адрес
    file_name = await get_file_name(user_data['chosen_file'])
    if not file_name:
        await message.answer("Извините, произошла ошибка при поиске файла.")
        return

    file_path = get_full_file_path(file_name)
    send_email(email_address, email_subject, email_body, file_path, file_name)

    await message.answer(email_send)
    # Переходим обратно в состояние CHOOSE_FILE
    await states.UserState.CHOOSE_FILE.set()
    await send_file_list(message, state)
