import sqlite3
from datetime import date, timedelta
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import (
    get_words_list_by_date,
    init_db,
    add_new_word,
    get_word,
    get_word_list,
    remove_word,
)
from app.models import ReviewStatus, Word


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Create a fresh in-memory database for every test."""
        self.conn = sqlite3.connect(":memory:")

        self.conn.execute("""
            CREATE TABLE vocabulary(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL UNIQUE,
                part_of_speech TEXT,
                phonetic TEXT,
                audio TEXT,
                meaning TEXT,
                example TEXT,
                repetitions INTEGER,
                ease_factor FLOAT,
                interval INTEGER,
                next_review DATE
            )
        """)

    def tearDown(self):
        """Close the database after every test."""
        self.conn.close()

    def create_word(self):
        return Word(
            "hello",
            "noun",
            "/həˈləʊ/",
            "hello.mp3",
            "a greeting",
            "Hello, how are you?",
        )

    def create_review_state(self):
        return ReviewStatus(0, 2.5, 0, next_review=date.today() + timedelta(days=1))

    # --------------------------------------------------
    # init_db
    # --------------------------------------------------

    def test_init_db_creates_table(self):
        with TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"

            init_db(str(db_path))

            conn = sqlite3.connect(db_path)

            result = conn.execute("""
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                AND name = 'vocabulary'
            """).fetchone()

            conn.close()

            self.assertEqual(result, ("vocabulary",))

    def test_init_db_can_be_called_twice(self):
        with TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test.db"

            init_db(str(db_path))
            init_db(str(db_path))

    # --------------------------------------------------
    # add_new_word
    # --------------------------------------------------

    def test_add_new_word(self):
        word = self.create_word()
        review_status = self.create_review_state()

        result = add_new_word(self.conn, word, review_status)
        self.assertEqual(result, True)

        return_word, return_review_status = get_word(self.conn, word.word)
        self.assertEqual(return_word, word)
        self.assertEqual(return_review_status, review_status)

    def test_add_duplicate_word(self):
        word = self.create_word()
        review_status = self.create_review_state()

        first_result = add_new_word(self.conn, word, review_status)
        second_result = add_new_word(self.conn, word, review_status)

        self.assertEqual(first_result, True)
        self.assertEqual(second_result, False)

        result_word, result_review_status = get_word(self.conn, word.word)
        self.assertEqual(result_word, word)
        self.assertEqual(result_review_status, review_status)

    # --------------------------------------------------
    # get_word
    # --------------------------------------------------

    def test_get_word(self):
        word = self.create_word()
        review_status = self.create_review_state()

        add_new_word(self.conn, word, review_status)

        word_result, review_result = get_word(self.conn, "hello")

        self.assertEqual(word_result, word)
        self.assertEqual(review_result, review_status)

    def test_get_word_not_found(self):
        result = get_word(self.conn, "hello")

        self.assertIsNone(result)

    # --------------------------------------------------
    # get_word_list
    # --------------------------------------------------

    def test_get_word_list(self):
        word1 = self.create_word()

        word2 = Word(
            "world",
            "noun",
            "/wɜːld/",
            "world.mp3",
            "the earth",
            "The world is beautiful.",
        )
        review_status = self.create_review_state()

        add_new_word(self.conn, word1, review_status)
        add_new_word(self.conn, word2, review_status)

        result = get_word_list(self.conn)

        self.assertEqual(result, [word1, word2])

    def test_get_word_list_empty(self):
        result = get_word_list(self.conn)

        self.assertEqual(result, [])

    # --------------------------------------------------
    # remove_word
    # --------------------------------------------------

    def test_remove_word(self):
        word = self.create_word()
        review_status = self.create_review_state()

        add_new_word(self.conn, word, review_status)

        remove_word(self.conn, "hello")

        result = get_word(self.conn, "hello")

        self.assertIsNone(result)

    def test_remove_word_not_found(self):
        # The function currently only prints an error.
        # This test makes sure it doesn't raise an exception.
        remove_word(self.conn, "hello")

    def test_get_word_list_by_date(self):
        word1 = self.create_word()
        word2 = Word(
            "world",
            "noun",
            "/wɜːld/",
            "world.mp3",
            "the earth",
            "The world is beautiful.",
        )
        review_status = self.create_review_state()

        add_new_word(self.conn, word1, review_status)
        add_new_word(self.conn, word2, review_status)

        word_list = get_words_list_by_date(
            self.conn, date=date.today() + timedelta(days=1)
        )
        self.assertEqual(word_list, [(word1, review_status), (word2, review_status)])

    def test_get_word_list_by_date_dif_date(self):
        word1 = self.create_word()
        review_status_1 = self.create_review_state()
        word2 = Word(
            "world",
            "noun",
            "/wɜːld/",
            "world.mp3",
            "the earth",
            "The world is beautiful.",
        )
        review_status_2 = ReviewStatus(1, 2.5, 3, date.today() + timedelta(days=2))

        add_new_word(self.conn, word1, review_status_1)
        add_new_word(self.conn, word2, review_status_2)

        word_list = get_words_list_by_date(
            self.conn, date=date.today() + timedelta(days=1)
        )
        self.assertEqual(word_list, [(word1, review_status_1)])

    def test_get_word_list_by_date_empty_date(self):
        word1 = self.create_word()
        review_status_1 = self.create_review_state()
        word2 = Word(
            "world",
            "noun",
            "/wɜːld/",
            "world.mp3",
            "the earth",
            "The world is beautiful.",
        )
        review_status_2 = ReviewStatus(1, 2.5, 3, date.today() + timedelta(days=2))

        add_new_word(self.conn, word1, review_status_1)
        add_new_word(self.conn, word2, review_status_2)

        word_list = get_words_list_by_date(
            self.conn, date=date.today() + timedelta(days=3)
        )
        self.assertListEqual(word_list, [])


if __name__ == "__main__":
    unittest.main()
