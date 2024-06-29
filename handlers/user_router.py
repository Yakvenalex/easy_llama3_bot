from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from create_bot import bot, client_groq
from db_handler.db_funk import (get_user_data, insert_user, clear_dialog,
                                add_message_to_dialog_history, get_dialog_status)
from keyboards.kbs import start_kb, stop_speak
from utils.utils import get_now_time
from aiogram.utils.chat_action import ChatActionSender

user_router = Router()


# хендлер команды старт
@user_router.message(Command(commands=['start', 'restart']))
async def cmd_start(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        user_info = await get_user_data(user_id=message.from_user.id)

    if len(user_info) == 0:
        await insert_user(user_data={
            'user_id': message.from_user.id,
            'full_name': message.from_user.full_name,
            'user_login': message.from_user.username,
            'in_dialog': False,
            'date_reg': get_now_time()
        })
        await message.answer(text='Привет! Давай начнем общаться. Для этого просто нажми на кнопку "Начать диалог"',
                             reply_markup=start_kb())
    else:
        await clear_dialog(user_id=message.from_user.id, dialog_status=False)
        await message.answer(text='Диалог очищен. Начнем общаться?', reply_markup=start_kb())


# Хендлер для начала диалога
@user_router.message(F.text.lower().contains('начать диалог'))
async def start_speak(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await clear_dialog(user_id=message.from_user.id, dialog_status=True)
        await message.answer(text='Диалог начат. Введите ваше сообщение:', reply_markup=stop_speak())


@user_router.message(F.text.lower().contains('завершить диалог'))
async def start_speak(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        await clear_dialog(user_id=message.from_user.id, dialog_status=False)
        await message.answer(text='Диалог очищен! Начнем общаться?', reply_markup=start_kb())


# Хендлер для обработки текстовых сообщений
@user_router.message(F.text)
async def handle_message(message: Message):
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        check_open = await get_dialog_status(message.from_user.id)
        if check_open is False:
            await message.answer(text='Для того чтоб начать общение со мной, пожалуйста, нажмите на кнопку '
                                      '"Начать диалог".', reply_markup=start_kb())
            return
    async with ChatActionSender.typing(bot=bot, chat_id=message.from_user.id):
        # формируем словарь с сообщением пользователя
        user_msg_dict = {"role": "user", "content": message.text}

        # сохраняем сообщение в базу данных и получаем историю диалога
        dialog_history = await add_message_to_dialog_history(user_id=message.from_user.id,
                                                             message=user_msg_dict,
                                                             return_history=True)

        # отправляем сообщение пользователя ассистенту и ждем ответ
        chat_completion = client_groq.chat.completions.create(messages=dialog_history, model="llama3-70b-8192")

        # отправляем ответ ассистента пользователю
        await message.answer(text=chat_completion.choices[0].message.content, reply_markup=stop_speak())

    # формируем словарь с сообщением ассистента
    assistant_msg = {"role": "assistant", "content": message.text}

    # сохраняем сообщение ассистента в базу данных
    await add_message_to_dialog_history(user_id=message.from_user.id, message=assistant_msg,
                                        return_history=False)