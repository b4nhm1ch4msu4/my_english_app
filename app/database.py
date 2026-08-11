import sqlite3
import logging
from dataclasses import asdict
from app.logger import setup_logging
from app.models import Word
from app.dictionary import lookup

DB_PATH = "data/vocabulary.db"
DB_TABLE_NAME = "vocabulary"

logger = logging.getLogger(__name__)


def init_db(db_path: str):
    logger.info(f"Init database : {db_path}")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vocabulary(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            part_of_speech TEXT,
            phonetic TEXT,
            audio TEXT,
            meaning TEXT,
            example TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_new_word(conn: sqlite3.Connection, word: Word):
    logger.info(f"Add '{word.word}' to database")
    w = get_word(conn, word.word)
    if w is None:
        logger.info(f"'{word.word}' not exist in database, create new one")
        cur = conn.cursor()
        cur.execute(
            f"""
            INSERT INTO {DB_TABLE_NAME} (
                word,
                part_of_speech,
                phonetic,
                audio,
                meaning,
                example
            ) VALUES(
                :word,
                :part_of_speech,
                :phonetic,
                :audio,
                :meaning,
                :example
            )
            """,
            asdict(word),
        )
        conn.commit()
        return True
    else:
        logger.warning(f"'{word.word}' exist in database, don't create")
        return False


def get_word(conn: sqlite3.Connection, word: str):
    logger.info(f"Finding '{word}' in database ....")
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT 
            word,
            part_of_speech,
            phonetic,
            audio,
            meaning,
            example        
        FROM {DB_TABLE_NAME} WHERE word = ?
        """,
        (word,),
    )
    row = cur.fetchone()
    if row:
        logger.info(f"Found '{word}' in database.")
        return Word(*row)
    logger.warning(f"NOT FOUND '{word}' in database")
    return None


def get_word_list(conn: sqlite3.Connection):
    logger.info(f"Get all words in list:")
    word_list = []
    cur = conn.cursor()
    cur.execute(f"""
        SELECT 
            word,
            part_of_speech,
            phonetic,
            audio,
            meaning,
            example        
        FROM {DB_TABLE_NAME}
        """)
    return [Word(*row) for row in cur.fetchall()]


def remove_word(conn: sqlite3.Connection, word: str):
    logger.info(f"Remove {word} in database")
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {DB_TABLE_NAME} WHERE word = ?", (word,))
    conn.commit()
    if cur.rowcount == 1:
        logger.info(f"'{word}' was removed from database.")
        return True
    else:
        logger.warning(
            f"FAIL to remove '{word}' from database. '{word}' may not exist in database."
        )
        return False


def main():
    setup_logging()
    init_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    new_word1 = lookup("hello")
    new_word2 = lookup("computer")
    new_word3 = lookup("image")
    if new_word1:
        res = add_new_word(conn, new_word1)
    if new_word2:
        res = add_new_word(conn, new_word2)

    if new_word3:
        res = add_new_word(conn, new_word3)
    word_list = get_word_list(conn)

    remove_word(conn, "hello")
    word_list = get_word_list(conn)
    remove_word(conn, "adab")
    conn.close()


if __name__ == "__main__":
    main()
