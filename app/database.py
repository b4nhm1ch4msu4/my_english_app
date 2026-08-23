import sqlite3
import logging
from datetime import date, timedelta
from dataclasses import asdict
from app.logger import setup_logging
from app.models import ReviewStatus, Word
from app.dictionary import lookup
from app.config import DB_TABLE_NAME,DB_PATH

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
            example TEXT,
            repetitions INTEGER,
            ease_factor FLOAT,
            interval INTEGER,
            next_review DATE
        )
    """)
    conn.commit()
    conn.close()


def get_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def add_new_word(conn: sqlite3.Connection, word: Word, review_status: ReviewStatus):
    logger.info(f"Add '{word.word}' to database")
    w,_ = get_word(conn, word.word)
    if w is None:
        word_info_dic = asdict(word) | asdict(review_status)
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
                example,
                repetitions,
                ease_factor,
                interval,
                next_review

            ) VALUES(
                :word,
                :part_of_speech,
                :phonetic,
                :audio,
                :meaning,
                :example,
                :repetitions,
                :ease_factor,
                :interval,
                :next_review
            )
            """,
            word_info_dic,
        )
        conn.commit()
        return True
    else:
        logger.warning(f"'{word.word}' exist in database, don't create")
        return False


def get_word(conn: sqlite3.Connection, word: str):
    logger.info(f"Finding '{word}' in database ....")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT 
            word,
            part_of_speech,
            phonetic,
            audio,
            meaning,
            example,
            repetitions,
            ease_factor,
            interval,
            next_review
        FROM {DB_TABLE_NAME} WHERE word = ?
        """,
        (word,),
    )
    row = cur.fetchone()
    if row:
        logger.info(f"Found '{word}' in database.")
        word_obj = Word(
            word=row["word"],
            part_of_speech=row["part_of_speech"],
            phonetic=row["phonetic"],
            audio=row["audio"],
            meaning=row["meaning"],
            example=row["example"],
        )

        review_status = ReviewStatus(
            repetitions=row["repetitions"],
            ease_factor=row["ease_factor"],
            interval=row["interval"],
            next_review=date.fromisoformat(row["next_review"]),
        )
        return word_obj, review_status
    logger.warning(f"NOT FOUND '{word}' in database")
    return None,None


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


def get_words_list_by_date(conn: sqlite3.Connection, date: date):
    logger.info(f"Get words list of today: {date}")
    words_list = []
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        f"""
        SELECT 
            word,
            part_of_speech,
            phonetic,
            audio,
            meaning,
            example,
            repetitions,
            ease_factor,
            interval,
            next_review
        FROM {DB_TABLE_NAME} WHERE next_review <= ?
        """,
        (date,),
    )
    for row in cur.fetchall():
        if row:
            word_obj = Word(
                word=row["word"],
                part_of_speech=row["part_of_speech"],
                phonetic=row["phonetic"],
                audio=row["audio"],
                meaning=row["meaning"],
                example=row["example"],
            )

            review_status = ReviewStatus(
                repetitions=row["repetitions"],
                ease_factor=row["ease_factor"],
                interval=row["interval"],
                next_review=date.fromisoformat(row["next_review"]),
            )
            words_list.append((word_obj, review_status))
    return words_list


def update_review_status(conn, word: Word, new_review_status: ReviewStatus):
    # TODO: update review status of word after learning
    pass


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
    review_status = ReviewStatus(
        0, 2.5, 0, next_review=date.today() + timedelta(days=1)
    )
    if new_word1:
        res = add_new_word(conn, new_word1, review_status)
    if new_word2:
        res = add_new_word(conn, new_word2, review_status)
    if new_word3:
        res = add_new_word(conn, new_word3, review_status)
    word_list = get_word_list(conn)

    remove_word(conn, "hello")
    word_list = get_word_list(conn)
    remove_word(conn, "adab")
    conn.close()


if __name__ == "__main__":
    main()
