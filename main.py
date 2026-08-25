import sqlite3

from app.logger import setup_logging
from app.dictionary import lookup
from app.tui.menu import (
    show_main_menu,
    learn_today_opt,
    add_word_opt,
    vocabulary_opt,
    search_word_opt,
    clear_screen
)
from app.database import get_connection, init_db
from app.config import DB_PATH


def main():
    setup_logging()
    init_db(DB_PATH)
    conn = get_connection(DB_PATH)
    try:
        while True:
            clear_screen()
            show_main_menu()

            choice = input("Choose an option: ").strip()

            if choice == "1":
                learn_today_opt(conn)

            elif choice == "2":
                add_word_opt(conn)

            elif choice == "3":
                vocabulary_opt(conn)

            elif choice == "4":
                search_word_opt()

            elif choice == "5":
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid option.")
                input("Press Enter to continue...")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
