import aiohttp
from app.settings import (WORDS_API_URL_USER_DICTIONARIES, WORDS_API_URL_USER_REPLY, WORDS_API_URL_USER_VERIFY,
                          WORDS_API_URL_UPDATE_WORD_FILE_ID)


async def get_random(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(WORDS_API_URL_USER_DICTIONARIES + str(telegram_id)) as response:
            return await response.json()


async def put_answer(data, word_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(WORDS_API_URL_USER_REPLY + str(word_id), json=data):
            pass


async def verify_user(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(WORDS_API_URL_USER_VERIFY + str(telegram_id)) as response:
            return await response.json()


async def update_word_file_id(word_id, data):
    async with aiohttp.ClientSession() as session:
        async with session.put(WORDS_API_URL_UPDATE_WORD_FILE_ID + str(word_id), json=data):
            pass
