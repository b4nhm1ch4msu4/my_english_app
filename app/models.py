from dataclasses import dataclass

@dataclass
class Word:
    word: str
    phonetic: str
    audio: str
    meanings: list[str]
    example: list[str]
