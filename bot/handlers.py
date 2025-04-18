from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from AI.init import manager
from AI.chat import new_text_message, new_photo_message, category_check, create_db, new_table
from bot.authorization import authorization
import os
from bot.speech_recognition_module import voice_to_text
from bot.extract_text_from_image import extract_text_from_image
import requests
import sqlite3
from bot import keyboads as kb


router = Router()

class TableResponse(StatesGroup):
    response_text = State()


@router.message(CommandStart())
async def start(message: Message):
    if authorization(message.from_user.id):
        await message.answer("Приветствую, Владислав!", reply_markup=kb.new_table())


@router.message(Command("clear_memory"))
async def clear(message: Message):
    if authorization(message.from_user.id):
        manager.clear_memory()
        db = sqlite3.connect("db/database.db")
        cur = db.cursor()
        cur.execute("DELETE FROM Finance")
        db.commit()
        await message.answer("Память очищена.", reply_markup=kb.new_table())


@router.message(Command("balance"))
async def balance(message: Message):
    if authorization(message.from_user.id):
        url = 'https://api.proxyapi.ru/proxyapi/balance'
        headers = {
            'Authorization': f'Bearer {os.getenv("AI_TOKEN")}'
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        await message.answer(f"{int(data['balance'])} рублей", reply_markup=kb.new_table())


@router.message(Command("db"))
async def balance(message: Message):
    if authorization(message.from_user.id):
        await create_db()
        file = FSInputFile("db/database.db")
        await message.bot.send_document(chat_id=message.chat.id, document=file)


@router.message(lambda message: message.media_group_id)
async def handle_media_group(message: Message):
    if authorization(message.from_user.id):
        await message.answer("Обрабатываю ваше фото...")
        if message.photo:
            photo_id = message.photo[-1].file_id
            file = await message.bot.get_file(photo_id)
            file_path = file.file_path
            name_file = "bot/files/photo.png"
            await message.bot.download_file(file_path, name_file)

            text = extract_text_from_image()

            gpt_text = await new_photo_message(text)
            await message.answer(gpt_text, reply_markup=kb.new_table())

            os.remove("bot/files/photo.png")


@router.message(lambda message: message.photo)
async def handle_photo(message: Message):
    if authorization(message.from_user.id):
        await message.answer("Обрабатываю ваше фото...")
        await message.bot.send_chat_action(message.chat.id, "typing")
        photo_id = message.photo[-1].file_id
        file = await message.bot.get_file(photo_id)
        file_path = file.file_path
        name_file = "bot/files/photo.png"
        await message.bot.download_file(file_path, name_file)

        text = extract_text_from_image()

        print("Распознанный текст: " + text)

        gpt_text = await new_photo_message(text)
        await message.answer(gpt_text, reply_markup=kb.new_table())

        os.remove("bot/files/photo.png")


@router.message(lambda message: message.voice)
async def handle_audio(message: Message):
    if authorization(message.from_user.id):
        await message.answer("Обрабатываю ваш аудио запрос...")
        await message.bot.send_chat_action(message.chat.id, "typing")
        voice = message.voice
        file = await message.bot.get_file(voice.file_id)
        file_path = file.file_path
        await message.bot.download_file(file_path, "bot/files/audio.ogg")
        text = voice_to_text()
        if text:
            os.remove("bot/files/audio.ogg")
            os.remove("bot/files/audio.wav")
            gpt_text = await new_text_message(text)
            await message.answer(gpt_text, reply_markup=kb.new_table())
            check = category_check()
            if check:
                await message.answer(check, reply_markup=kb.new_table())

        else:
            await message.answer("Извините, не могу разобрать вашу речь...", reply_markup=kb.new_table())
            
            
@router.message(lambda message: message.text == "Создать таблицу")         
@router.message(Command("table"))
async def handle_table(message: Message, state: FSMContext):
    await message.answer("Введи запрос для создания таблицы")
    await state.set_state(TableResponse.response_text)
    
@router.message(TableResponse.response_text)
async def create_table(message: Message, state: FSMContext):
    await message.answer("Формирую таблицу по вашему запросу...")
    await message.bot.send_chat_action(message.chat.id, "typing")
    await state.clear()
    await new_table(message.text)
    await message.bot.send_chat_action(message.chat.id, "upload_document")
    await message.answer_document(document=FSInputFile("bot/files/table.csv"))
    await message.bot.send_chat_action(message.chat.id, "upload_document")
    await message.answer_document(document=FSInputFile("bot/files/table.xlsx"))
    os.remove("bot/files/table.csv")
    os.remove("bot/files/table.xlsx")
    await message.answer("Таблицы готовы!", reply_markup=kb.new_table())  


@router.message()
async def handle_text(message: Message):
    if authorization(message.from_user.id):
        await message.bot.send_chat_action(message.chat.id, "typing")
        gpt_text = await new_text_message(message.text)
        await message.answer(gpt_text, reply_markup=kb.new_table())
        check = await category_check()
        if check:
            await message.answer(check, reply_markup=kb.new_table())
