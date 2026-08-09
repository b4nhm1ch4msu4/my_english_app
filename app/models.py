from dataclasses import dataclass

@dataclass
class Word:
    word: str
    part_of_speech: str
    phonetic: str
    audio: str
    meaning: str
    example: str
