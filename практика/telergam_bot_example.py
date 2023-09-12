""" 
Делал на основании статьи тут:
https://tproger.ru/articles/kak-napisat-telegram-bota-na-python-delaem-remajnder

Порядок выполнения:
1. Найти в Telegram BotFather и создать бота, я создал под именем PythonBasicTestBot
Он пришлет сообщение типа такого:
    Done! Congratulations on your new bot. You will find it at t.me/PythonBasicTestBot. 
    You can now add a description, about section and profile picture for your bot, 
    see /help for a list of commands. By the way, when you've finished creating your 
    cool bot, ping our Bot Support if you want a better username for it. 
    Just make sure the bot is fully operational before you do this.

    Use this token to access the HTTP API:
    ******** - здесь будет токен
    Keep your token secure and store it safely, it can be used by anyone to control your bot.

2. Создать виртуальное окружение (venv), это чтобы не засорять ваш интерпретатор,
т.к. будет ставится специальная библиотека для работы с Telegram и установить aiogram.
Лучше ставить не последнюю версию, т.к. она еще не стабильна, а предыдущую:
pip install aiogram==2.23.1

3. Скопировать код и запустить его на вашем ПК через $ python <имя файла с кодом>.py

Это все. Этот бот просто будет отвечать "Привет, <ваше имя>" на команду /start в чате и 
периодически слать напоминалки про программирование. Но можно реализовать любое поведение.

Здесь используется библиотека asyncio, которая отвечает за реализацию асинхронного 
программирования, мы ее не проходили, можно почитать, например, на Хабре:
https://habr.com/ru/companies/wunderfund/articles/700474/. 


А дальше можно наполнять вашего бота различной функциональностью.

"""

import time
import logging
import asyncio

from aiogram import Bot, Dispatcher, executor, types

TOKEN = "ЗДЕСЬ ДОЛЖЕН БЫТЬ ВАШ ТОКЕН"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')

    await message.reply(f"Привет, {user_full_name}!")

    for i in range(7):
        await asyncio.sleep(60*10)
        await bot.send_message(user_id, f"Программировал ли ты сегодня, {user_name}?")

if __name__ == '__main__':
    executor.start_polling(dp)