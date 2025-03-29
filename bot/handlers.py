from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from AI.init import manager
from AI.chat import new_text_message, new_photo_message, category_check
from bot.authorization import authorization
import os
from bot.speech_recognition_module import voice_to_text
from bot.extract_text_from_image import extract_text_from_image
import requests


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    if authorization(message.from_user.id):
        await message.answer("Приветствую, Владислав!")


@router.message(Command("clear_memory"))
async def clear(message: Message):
    if authorization(message.from_user.id):
        manager.clear_memory()
        await message.answer("Память очищена.")


@router.message(Command("balance"))
async def balance(message: Message):
    url = 'https://api.proxyapi.ru/proxyapi/balance'
    headers = {
        'Authorization': f'Bearer {os.getenv("AI_TOKEN")}'
    }
    response = requests.get(url, headers=headers)
    data = response.json()
    await message.answer(f"{int(data["balance"])} рублей")


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
            await message.answer(gpt_text)

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

        gpt_text = await new_photo_message(text)
        await message.answer(gpt_text)

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
            await message.answer(gpt_text)
            check = category_check()
            if check:
                await message.answer(check)

        else:
            await message.answer("Извините, не могу разобрать вашу речь...")


@router.message()
async def handle_text(message: Message):
    if authorization(message.from_user.id):
        await message.bot.send_chat_action(message.chat.id, "typing")
        gpt_text = await new_text_message(message.text)
        await message.answer(gpt_text)
        check = await category_check()
        if check:
            await message.answer(check)
