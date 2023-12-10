from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from app.service import requests
from app.keyboards import quiz as quiz_keyboards
from app.service import json_fetcher, data_struct
from app.settings import (available_type_of_quiz, available_type_of_help_message, WORDS_API_URL_MEDIA,
                          MESSAGE_CHOOSE_TYPE_OF_QUIZ, MESSAGE_USER_DOES_NOT_EXIST, MESSAGE_FINISH_QUIZ,
                          MESSAGE_WRONG_ANSWER, MESSAGE_QUESTION)
from app.quiz_game_play import GamePlay
from aiogram.types import URLInputFile
from aiogram.exceptions import TelegramBadRequest
from app.bot import bot


router = Router()


class Quiz(StatesGroup):
    choosing_type_of_quiz = State()
    game_play = State()


@router.message(Command("quiz"))
async def start_quiz(message: Message, state: FSMContext):
    verification_user = await requests.verify_user(message.from_user.id)
    if verification_user['verify'] == 'True':
        await state.set_state(Quiz.choosing_type_of_quiz)
        await message.answer(
            text=MESSAGE_CHOOSE_TYPE_OF_QUIZ,
            reply_markup=quiz_keyboards.get_keyboard_choose_type_of_quiz(available_type_of_quiz)
        )
    else:
        await state.clear()
        text_message = MESSAGE_USER_DOES_NOT_EXIST + str(message.from_user.id)
        await message.answer(text_message)


@router.callback_query(Quiz.choosing_type_of_quiz, F.data.in_(available_type_of_quiz))
async def start_quiz1(callback: types.CallbackQuery, state: FSMContext):
    type_of_quiz = callback.data.lower()
    quiz_list = await json_fetcher.get_quiz_list(callback.from_user.id, type_of_quiz=callback.data.lower())
    game_play = GamePlay(quiz_list)
    await state.update_data(game_play=game_play, type_of_quiz=callback.data.lower())

    current_user_question: data_struct.UserWord = await game_play.get_current_quiz_question()
    keyboard = quiz_keyboards.get_help_keyboard(available_type_of_help_message)
    await callback.message.answer(MESSAGE_QUESTION + current_user_question.word, reply_markup=keyboard)
    if type_of_quiz == 'en':
        if current_user_question.file_id:
            try:
                file = await bot.get_file(current_user_question.file_id)
                result = await callback.message.answer_audio(current_user_question.file_id,
                                                             title=current_user_question.word_origin)

            except TelegramBadRequest:
                file = URLInputFile(WORDS_API_URL_MEDIA + current_user_question.word + '.mp3')
                result = await callback.message.answer_audio(file, title=current_user_question.word_origin)
                await requests.update_word_file_id(current_user_question.word_pk, {"file_id": result.audio.file_id})

        else:
            file = URLInputFile(WORDS_API_URL_MEDIA + current_user_question.word_origin + '.mp3')
            result = await callback.message.answer_audio(file, title=current_user_question.word_origin)
            await requests.update_word_file_id(current_user_question.word_pk, {"file_id": result.audio.file_id})

    await state.set_state(Quiz.game_play)
    await callback.answer()


@router.message(Quiz.game_play, F.text.in_(available_type_of_help_message))
async def get_help_message(message: Message, state: FSMContext):
    user_data = await state.get_data()
    game_play: GamePlay = user_data['game_play']
    current_user_question: data_struct.UserWord = await game_play.get_current_quiz_question()

    if message.text == available_type_of_help_message[0]: #"Get Example"
        await message.answer(text=current_user_question.usage_example)
    elif message.text == available_type_of_help_message[1]: #"Get Part Of Speach"
        await message.answer(text=current_user_question.part_of_speach)


@router.message(Quiz.game_play)
async def food_chosen_incorrectly(message: Message, state: FSMContext):
    user_data = await state.get_data()
    game_play: GamePlay = user_data['game_play']
    type_of_quiz = user_data['type_of_quiz']
    result, end_of_game, previous_user_word_pk = await game_play.check_user_answer(answer=message.text)
    keyboard = quiz_keyboards.get_help_keyboard(available_type_of_help_message)

    if result and not end_of_game:
        current_user_question: data_struct.UserWord = await game_play.get_current_quiz_question()
        await message.answer(MESSAGE_QUESTION + current_user_question.word, reply_markup=keyboard)
        if type_of_quiz == 'en':
            if current_user_question.file_id:
                try:
                    file = await bot.get_file(current_user_question.file_id)
                    result = await message.answer_audio(current_user_question.file_id,
                                                        title=current_user_question.word_origin)
                except TelegramBadRequest:
                    file = URLInputFile(WORDS_API_URL_MEDIA + current_user_question.word_origin + '.mp3')
                    result = await message.answer_audio(file, title=current_user_question.word_origin)
                    await requests.update_word_file_id(current_user_question.word_pk, {"file_id": result.audio.file_id})
            else:
                file = URLInputFile(WORDS_API_URL_MEDIA + current_user_question.word_origin + '.mp3')
                result = await message.answer_audio(file, title=current_user_question.word_origin)
                await requests.update_word_file_id(current_user_question.word_pk, {"file_id": result.audio.file_id})
        await state.update_data(game_play=game_play)
        await requests.put_answer({"answer": "True"}, previous_user_word_pk)
    elif result and end_of_game:
        await message.answer(text=MESSAGE_FINISH_QUIZ, reply_markup=ReplyKeyboardRemove())
        await requests.put_answer({"answer": "True"}, previous_user_word_pk)
        await state.clear()
    else:
        await message.answer(MESSAGE_WRONG_ANSWER)
        await requests.put_answer({"answer": "False"}, previous_user_word_pk)

