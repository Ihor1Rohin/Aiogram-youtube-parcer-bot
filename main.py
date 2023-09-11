from aiogram import Bot,types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from selenium import webdriver
from selenium.webdriver.common.by import By
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from config import Token
from time import sleep
import emoji
from selenium.webdriver.chrome.options import Options
from random import randint
import os
from yt_dlp import YoutubeDL

button_1 = KeyboardButton("/Пошук")
button_2 = KeyboardButton("/Принцип_роботи")
button_3 = KeyboardButton("/Стоп")
button_4 = KeyboardButton("/Випадкове_число")
button_5 = KeyboardButton("/Скачати")
button_5_1 = KeyboardButton("/360p")
button_5_2 = KeyboardButton("/720p")
button_5_3 = KeyboardButton("/1080p")
button_5_4 = KeyboardButton("/MP3")
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_second = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_random = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_download=ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(button_1).add(button_2).add(button_5)
keyboard_second.add(button_3)
keyboard_random.add(button_4).add(button_3)
keyboard_download.add(button_5_1).add(button_5_2).add(button_5_3).add(button_5_4)

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
storage = MemoryStorage()
bot = Bot(token = Token)
dp = Dispatcher(bot,storage=storage)

class FSM_name_of_video(StatesGroup):
    name = State()
    amount = State()

class FSM_Load(StatesGroup):
    link = State()

@dp.message_handler(commands = ["start"])
async def cmd_start(message: types.Message):
    await message.answer(emoji.emojize("Привіт :raised_hand: " + message.from_user.first_name + " ! Я бот створений Ігорем. \nДля того щоб подивитися як Я працюю, натисність кнопку Принцип роботи"), reply_markup=keyboard)

@dp.message_handler(commands = 'Принцип_роботи')
async def cmd_byak(message: types.Message):
    await message.answer("Для того щоб розпочати користуватися Вам потрібно натиснути кнопку Пошук, ввести назву відео, яке Ви шукаєте, а потім написати кількість відео для пошуку")

@dp.message_handler(commands=["Стоп"], state='*')
async def cancel(message: types.Message, state: FSMContext) -> None:
    vidmina = await state.get_state()
    if vidmina is None:
        return
    await message.reply(emoji.emojize('Відміняю :sparkles:'), reply_markup=keyboard)
    await state.finish()

@dp.message_handler(commands= "Скачати", state=None)
async def send_link(message: types.Message):
    await FSM_Load.link.set()
    await message.answer("Надійшли мені посилання на відео",reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(state=FSM_Load.link)
async def save_link(message:types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['link'] = message.text
    await FSM_Load.next()
    await message.answer("Оберіть тип відео", reply_markup=keyboard_download)
    return data['link']

                                        #360p///////////////////////////////////////////
@dp.message_handler(commands="360p", state=None)
async def choose(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer("Заряджаємо ваше відео :)", reply_markup=types.ReplyKeyboardRemove())
        res = "360p"
        a = str(12)
        driver.get(data['link'])
        sleep(2)
        title_element = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
        byak = title_element.text
        byak = byak.replace("'", "").replace('"', '').replace('|', '_').replace(' | ', '_').replace('/', '_').replace(
            '\\', '_').replace('*', '_').replace('?', '').replace('<', '').replace('>', '_').replace(':', '').replace(
            ';', '').replace('.', '').strip()
        searched_name = f"{byak}.mp4"
        ydl_opts = {
            'format': f'bestvideo[height={res}]+bestaudio/best',
            'outtmpl': f'E:/Python/{a}/{searched_name}',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(data['link'])
        absolute_folder_path = os.path.join('E:/Python/12')
        video_file_path = os.path.join(absolute_folder_path, searched_name)

        with open(video_file_path, "rb") as video:
            await bot.send_video(message.chat.id, video, caption="Video", parse_mode="Markdown")
        os.remove(video_file_path)
        await message.answer("Ваше відео чекає на вас!", reply_markup=keyboard)
        await state.finish()

@dp.message_handler(commands="MP3", state=None)
async def choose(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        youtube_link = data['link']
        await message.answer("Заряджаємо ваше відео :)", reply_markup=types.ReplyKeyboardRemove())
        a = str(12)
        driver.get(data['link'])
        sleep(2)
        title_element = driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
        byak = title_element.text
        byak = byak.replace("'", "").replace('"', '').replace('|', '_').replace(' | ', '_').replace('/', '_').replace(
            '\\', '_').replace('*', '_').replace('?', '').replace('<', '').replace('>', '_').replace(':', '').replace(
            ';', '').replace('.', '').strip()
        searched_name = f"{byak}.mp3"
        ydl_opts = {
            'format': f'bestaudio/best',
            'outtmpl': f'E:/Python/{a}/{searched_name}',
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(data['link'])
        absolute_folder_path = os.path.join('E:/Python/12')
        audio_file_path = os.path.join(absolute_folder_path, searched_name)
        with open(audio_file_path, "rb") as audio:
            await bot.send_video(message.chat.id, audio, caption="Audio", parse_mode="Markdown")
        os.remove(audio_file_path)
        await message.answer("Ваше відео чекає на вас!", reply_markup=keyboard)
        await state.finish()
                        #72000000000000000000000000000000000000000000000p :)

@dp.message_handler(commands=["стоп"], state='*')
async def cancel(message: types.Message, state: FSMContext) -> None:
    vidmina = await state.get_state()
    if vidmina is None:
        return
    await message.reply(emoji.emojize('Відміняю :sparkles:'), reply_markup=keyboard)
    await state.finish()

@dp.message_handler(commands=["Випадкове_число"], state=FSM_name_of_video.amount)
async def magic(message: types.Message, state: FSMContext):
    magic_number = randint(2, 9)
    async with state.proxy() as data:
        data['amount'] = magic_number
    await message.reply('Ваше випадкове число - ' + str(magic_number))
    video_href = "https://www.youtube.com/results?search_query=" + data['name']
    driver.get(video_href)
    sleep(2)
    videos = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
    a = False
    await message.answer(emoji.emojize('Магія в процесі :sparkles:'))
    i = 1
    for i, video in enumerate(videos):
        if i < magic_number:
            video_link = video.get_attribute("href")
            await message.answer(video_link)
        else:
            break
    await message.answer(emoji.emojize('Магія була зроблена :sparkles:'), reply_markup=keyboard)
    await state.finish()

@dp.message_handler(commands='Пошук', state=None)
async def start_searching(message : types.Message):
    await FSM_name_of_video.name.set()
    await message.reply("Введіть назву відео ", reply_markup=keyboard_second)

@dp.message_handler(state=FSM_name_of_video.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSM_name_of_video.next()
    await message.answer("Введіть кількість відео",reply_markup=keyboard_random)

@dp.message_handler(state=FSM_name_of_video.amount)
async def amount_of_videos(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    if not isinstance(data['amount'],int):
        await state.finish()
    video_link = "https://www.youtube.com/results?search_query=" + data['name']
    driver.get(video_link)
    sleep(2)
    video_array = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
    for i,obj in enumerate(video_array):
        if i < int(data['amount']):
            link = obj.get_attribute("href")
            await message.answer(link)
        if i> int(data['amount']):
            break
    await message.answer(emoji.emojize('Магія була зроблена :sparkles:'),reply_markup=keyboard)
    await state.finish()



executor.start_polling(dp, skip_updates=True)