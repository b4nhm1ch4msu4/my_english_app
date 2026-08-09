from app.models import Word
import requests
import json


def lookup(input_word: str) -> Word | None:
    """
    Look up a word using the Free Dictionary API
    and return a Word object.

    API:
    https://dictionaryapi.dev/
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{input_word}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()

    if not data:
        return None

    entry = data[0]

    word = entry.get("word", input_word)
    phonetic = entry.get("phonetic", "")
    part_of_speech = ""
    audio = ""
    meaning = ""
    example = ""

    # Get phonetic and audio
    for phonetic_item in entry.get("phonetics", []):
        if not phonetic and phonetic_item.get("text"):
            phonetic = phonetic_item["text"]

        if not audio and phonetic_item.get("audio"):
            audio = phonetic_item["audio"]

        if phonetic and audio:
            break

    # Get meanings and examples
    for meaning_item in entry.get("meanings", []):
        part_of_speech = meaning_item.get("partOfSpeech", "")

        for definition_item in meaning_item.get("definitions", []):
            definition = definition_item.get("definition")
            example_item = definition_item.get("example")

            if example_item:
                example = example_item

            if definition:
                meaning = definition

            if example and meaning:
                break

    return Word(
        word=word,
        phonetic=phonetic,
        audio=audio,
        meaning=meaning,
        example=example,
        part_of_speech=part_of_speech,
    )
