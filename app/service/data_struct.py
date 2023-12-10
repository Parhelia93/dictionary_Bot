from dataclasses import dataclass


@dataclass
class UserWord:
    word_pk: int
    word: str
    file_id: str
    user_word_pk: int
    translate: str
    usage_example: str
    part_of_speach: str
    word_origin: str
