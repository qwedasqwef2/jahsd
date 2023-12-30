import asyncio
from pyrogram import Client, filters

from setts import *
from prompts import prompts

from gpt import gpt

import datetime
import re

from fuzzywuzzy import fuzz

swt = datetime.datetime.now()

app = Client("account", api_id=API_ID, api_hash=API_HASH)

texts = []

print("Welcome")


async def work(msg, word, TYPE) -> int:
    """

    Обработка сообщения

    """

    CHURL = str(msg.chat.id)
    UUS = msg.from_user.username

    if UUS == None:
        UUS = "юзернейма нет"
    else:
        UUS = f"@{UUS}"

    CHURL = "https://t.me/c/"+CHURL.replace("-100", "")

    msg_url = f"{CHURL}/{msg.id}"

    answer_text = f"Тип: \"#{TYPE}\"\n\n ID чата: {msg.chat.id}\n\n URL чата: {CHURL}\n\n ID пользователя: {msg.from_user.id}\n\n username пользователя: {UUS}\n\n Ссылка на сообщение: {msg_url}\n➖➖➖\n\n Детект-Слово: {word}\n➖➖➖Сообщение: \n\"{msg.text}\""

    print(answer_text)
    await app.send_message(send_ids.get(TYPE), answer_text)

    gpt_answer = str(gpt(prompts.get(TYPE)))
    if gpt_answer != "False":
        await msg.reply(gpt_answer)
    else:
        print("no_reply")

    return 0


@app.on_message()
async def analyze(_, message) -> None:
    """

    Функция для анализирования сообщения на наличие "вопросительных слов"

    """
    if message.text in texts[-10:]:
        return

    texts.append(message.text)

    for word in WORDS:
        if "[TYPE=" in word:
            TYPE = word.split("=")[1].replace("]", "")
            continue
        if fuzz.token_set_ratio(message.text, word) >= 90 \
                and len(str(message.text)) >= 10\
                or re.search(word.lower(), str(message.text).lower()) != None\
                and len(str(message.text)) >= 10:
            for banw in BANWORDS:
                if fuzz.token_set_ratio(message.text, banw) >= 80:
                    return
            await work(message, word, TYPE)
            break


app.run()