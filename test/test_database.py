import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import (
    init_db,
    add_new_word,
    get_word,
    get_word_list,
    remove_word,
)
from app.models import Word


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
                example TEXT
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

        result = add_new_word(self.conn, word)
        self.assertEqual(result, True)

        result = get_word(self.conn, word.word)
        self.assertEqual(result, word)

    def test_add_duplicate_word(self):
        word = self.create_word()

        first_result = add_new_word(self.conn, word)
        second_result = add_new_word(self.conn, word)

        self.assertEqual(first_result, True)
        self.assertEqual(second_result, False)

    # --------------------------------------------------
    # get_word
    # --------------------------------------------------

    def test_get_word(self):
        word = self.create_word()

        add_new_word(self.conn, word)

        result = get_word(self.conn, "hello")

        self.assertEqual(result, word)

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

        add_new_word(self.conn, word1)
        add_new_word(self.conn, word2)

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

        add_new_word(self.conn, word)

        remove_word(self.conn, "hello")

        result = get_word(self.conn, "hello")

        self.assertIsNone(result)

    def test_remove_word_not_found(self):
        # The function currently only prints an error.
        # This test makes sure it doesn't raise an exception.
        remove_word(self.conn, "hello")


if __name__ == "__main__":
    unittest.main()
