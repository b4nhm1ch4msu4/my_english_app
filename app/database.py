import sqlite3
from dataclasses import asdict
from app.models import Word
from app.dictionary import lookup

DB_PATH = "data/vocabulary.db"
DB_TABLE_NAME = "vocabulary"


def init_db(db_path: str):
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
    new_word = asdict(word)
    cur = conn.cursor()
    cur.execute(
        f"""
        INSERT INTO {DB_TABLE_NAME} (word,part_of_speech,phonetic,audio,meaning,example) VALUES(:word,:part_of_speech,:phonetic,:audio,:meaning,:example)
    """,new_word
    )
    conn.commit()


def get_meaning(conn: sqlite3.Connection, word: str):
    cur = conn.cursor()
    cur.execute(f"SELECT meaning FROM {DB_TABLE_NAME} WHERE word = ?", (word,))
    meaning = cur.fetchone()
    return meaning[0]


def main():
    init_db(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    new_word1 = lookup("hello")
    new_word2 = lookup("computer")
    new_word3 = lookup("image")
    if new_word1:
        # add_new_word(conn, new_word1)
        pass
    if new_word2:
        # add_new_word(conn, new_word2)
        pass

    print(get_meaning(conn, "computer"))
    conn.close()


if __name__ == "__main__":
    main()
