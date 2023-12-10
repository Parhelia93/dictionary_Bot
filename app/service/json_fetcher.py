from . import requests
from app.service.data_struct import UserWord


async def get_quiz_list(telegram_id: int, type_of_quiz: str) -> list[UserWord]:
    quiz_list = list()
    server_quiz_list = await requests.get_random(telegram_id)

    for user_word in server_quiz_list:
        if type_of_quiz == 'rus':
            word = user_word['translate']
            translate = user_word['user_word']['word']
        else:
            word = user_word['user_word']['word']
            translate = user_word['translate']

        quiz_list.append(
            UserWord(
                word_pk=user_word['user_word']['pk'],
                word=word,
                file_id=user_word['user_word']['telegram_file_id'],
                user_word_pk=user_word['pk'],
                translate=translate,
                usage_example=user_word['usage_example'],
                part_of_speach=user_word['part_of_speach'],
                word_origin=user_word['user_word']['word']
            )
        )
    return quiz_list
