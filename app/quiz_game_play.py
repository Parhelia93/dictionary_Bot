from app.service.data_struct import UserWord


class GamePlay:
    def __init__(self, quiz_list: list[UserWord]):
        self.quiz_list = quiz_list
        self.current_game_play_step = 0

    async def get_another_question(self) -> str:
        if self.current_game_play_step < len(self.quiz_list):
            return self.quiz_list[self.current_game_play_step].word

    async def check_user_answer(self, answer: str) -> list:
        result = [False, False, 0]
        result[2] = self.quiz_list[self.current_game_play_step].user_word_pk
        if self.quiz_list[self.current_game_play_step].translate == answer:
            self.current_game_play_step += 1
            result[0] = True
        else:
            result[0] = False

        result[1] = True if self.current_game_play_step == len(self.quiz_list) else False
        return result

    async def get_current_quiz_question(self):
        return self.quiz_list[self.current_game_play_step]






