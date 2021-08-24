# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import json
import requests
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


API = "https://api.sumanjay.cf/watch/query="

JOIN_BUTTONS = [
    InlineKeyboardButton(
        text='⚙ Join Updates Channel ⚙',
        url='https://telegram.me/FayasNoushad'
    )
]


@Client.on_message(filters.command(["info", "information"]), group=2)
async def get_command(bot, update):
    movie = requote_uri(update.text.split(" ", 1)[1])
    username = (await bot.get_me()).username
    keyboard = [
        InlineKeyboardButton(
            text="Click here",
            url=f"https://telegram.me/{username}?start={movie}"
        )
    ]
    await update.reply_text(
        text=f"**Click the button below**",
        reply_markup=InlineKeyboardMarkup([keyboard]),
        disable_web_page_preview=True,
        quote=True
    )


@Client.on_message(filters.private & filters.text & ~filters.via_bot & ~filters.edited)
async def get_movie_name(bot, update):
    if update.text.startswith("/"):
        return
    await get_movie(bot, update, update.text)


async def get_movie(bot, update, name):
    movie_name = requote_uri(name)
    movie_api = API + movie_name
    r = requests.get(movie_api)
    movies = r.json()
    keyboard = []
    number = 0
    for movie in movies:
        number += 1
        switch_text = movie_name + "+" + str(number)
        try:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=description(movie),
                        switch_inline_query_current_chat=switch_text
                    )
                ]
            )
        except:
            pass
    keyboard.append(JOIN_BUTTONS)
    await update.reply_text(
        text="Select required option",
        reply_markup=InlineKeyboardMarkup(keyboard),
        disable_web_page_preview=True,
        quote=True
    )




def thumb(movie):
    thumbnail = movie['movie_thumb'] if movie['movie_thumb'] else None
    return thumbnail
