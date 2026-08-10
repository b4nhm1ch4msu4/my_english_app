import re
import unittest
from unittest.mock import Mock, patch

from app.dictionary import lookup
from app.models import Word


class TestLookup(unittest.TestCase):

    def test_lookup_success(self):
        mock_api_response = [
            {
                "word": "hello",
                "phonetic": "həˈləʊ",
                "phonetics": [
                    {"text": "həˈləʊ", "audio": "https://example.com/hello.mp3"}
                ],
                "meanings": [
                    {
                        "partOfSpeech": "exclamation",
                        "definitions": [
                            {
                                "definition": "Used as a greeting.",
                                "example": "Hello, how are you?",
                            }
                        ],
                    },
                    {
                        "partOfSpeech": "noun",
                        "definitions": [
                            {
                                "definition": "An utterance of hello.",
                                "example": "She gave me a warm hello.",
                            }
                        ],
                    },
                ],
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("hello")

        self.assertIsInstance(result, Word)
        if result:
            self.assertEqual(result.word, "hello")
            self.assertEqual(result.phonetic, "həˈləʊ")
            self.assertEqual(result.audio, "https://example.com/hello.mp3")
            self.assertEqual(result.meaning, "Used as a greeting.")
            self.assertEqual(result.example, "Hello, how are you?")
            self.assertEqual(result.part_of_speech, "exclamation")

    def test_lookup_word_not_found(self):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = {
            "title": "No Definitions Found",
            "message": "Sorry pal, we couldn't find definitions for the word.",
        }

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("notarealword")

        self.assertIsNone(result)

    def test_lookup_empty_response(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = []

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("empty")

        self.assertIsNone(result)

    def test_lookup_missing_phonetic_uses_phonetics_text(self):
        mock_api_response = [
            {
                "word": "test",
                "phonetics": [{"text": "/test/", "audio": ""}],
                "meanings": [],
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("test")

        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.word, "test")
            self.assertEqual(result.phonetic, "/test/")
            self.assertEqual(result.audio, "")
            self.assertEqual(result.meaning, "")
            self.assertEqual(result.example, "")

    def test_lookup_missing_audio_returns_empty_string(self):
        mock_api_response = [
            {
                "word": "quiet",
                "phonetic": "/ˈkwaɪət/",
                "phonetics": [{"text": "/ˈkwaɪət/"}],
                "meanings": [
                    {
                        "partOfSpeech": "adjective",
                        "definitions": [{"definition": "Making little or no noise."}],
                    }
                ],
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("quiet")

        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.word, "quiet")
            self.assertEqual(result.phonetic, "/ˈkwaɪət/")
            self.assertEqual(result.audio, "")
            self.assertEqual(result.meaning, "Making little or no noise.")
            self.assertEqual(result.example, "")

    def test_lookup_definition_without_part_of_speech(self):
        mock_api_response = [
            {
                "word": "simple",
                "phonetic": "",
                "phonetics": [],
                "meanings": [
                    {
                        "definitions": [
                            {
                                "definition": "Easy to understand.",
                                "example": "This is a simple example.",
                            }
                        ]
                    }
                ],
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("simple")

        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.word, "simple")
            self.assertEqual(result.phonetic, "")
            self.assertEqual(result.audio, "")
            self.assertEqual(result.part_of_speech, "")
            self.assertEqual(result.meaning, "Easy to understand.")
            self.assertEqual(result.example, "This is a simple example.")

    def test_lookup_uses_input_word_if_word_missing(self):
        mock_api_response = [{"phonetic": "", "phonetics": [], "meanings": []}]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("fallback")

        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.word, "fallback")
            self.assertEqual(result.phonetic, "")
            self.assertEqual(result.audio, "")
            self.assertEqual(result.meaning, "")
            self.assertEqual(result.example, "")

    def test_lookup_multiple_phonetics_uses_first_available_audio(self):
        mock_api_response = [
            {
                "word": "hello",
                "phonetic": "",
                "phonetics": [
                    {"text": "/həˈləʊ/", "audio": ""},
                    {"text": "/hɛˈloʊ/", "audio": "https://example.com/audio-us.mp3"},
                ],
                "meanings": [],
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("hello")

        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.word, "hello")
            self.assertEqual(result.phonetic, "/həˈləʊ/")
            self.assertEqual(result.audio, "https://example.com/audio-us.mp3")
            self.assertEqual(result.meaning, "")
            self.assertEqual(result.example, "")

    def test_lookup_multiple_definitions(self):
        mock_api_response = [
            {
                "word": "run",
                "phonetic": "/rʌn/",
                "phonetics": [],
                "meanings": [
                    {
                        "partOfSpeech": "verb",
                        "definitions": [
                            {
                                "definition": "Move at a speed faster than a walk.",
                                "example": "I run every morning.",
                            },
                            {
                                "definition": "Manage or operate.",
                                "example": "She runs a company.",
                            },
                        ],
                    }
                ],
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("run")

        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.word, "run")
            self.assertEqual(result.phonetic, "/rʌn/")
            self.assertEqual(result.audio, "")
            self.assertEqual(
                result.meaning,
                "Move at a speed faster than a walk.",
            )
            self.assertEqual(result.example, "I run every morning.")

    def test_lookup_definition_without_example(self):
        mock_api_response = [
            {
                "word": "book",
                "phonetic": "/bʊk/",
                "phonetics": [],
                "meanings": [
                    {
                        "partOfSpeech": "noun",
                        "definitions": [{"definition": "A written or printed work."}],
                    }
                ],
            }
        ]

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_api_response

        with patch("app.dictionary.requests.get", return_value=mock_response):
            result = lookup("book")

        self.assertIsNotNone(result)
        if result:
            self.assertEqual(result.word, "book")
            self.assertEqual(result.phonetic, "/bʊk/")
            self.assertEqual(result.audio, "")
            self.assertEqual(result.meaning, "A written or printed work.")
            self.assertEqual(result.example, "")

    def test_lookup_calls_correct_api_url(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"word": "hello", "phonetics": [], "meanings": []}
        ]

        with patch(
            "app.dictionary.requests.get", return_value=mock_response
        ) as mock_get:
            lookup("hello")

        mock_get.assert_called_once_with(
            "https://api.dictionaryapi.dev/api/v2/entries/en/hello", timeout=10
        )


if __name__ == "__main__":
    unittest.main()
