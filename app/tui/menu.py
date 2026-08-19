from datetime import date
from app.dictionary import lookup
from app.database import (
    add_new_word,
    get_word_list,
    get_words_list_by_date,
    remove_word,
)
from app.models import Word, default_review_status, Quality


def show_main_menu():
    print()
    print("=" * 40)
    print("        English Learning App")
    print("=" * 40)
    print()
    print("1. Learn today")
    print("2. Add new word")
    print("3. My vocabulary")
    print("4. Search word")
    print("5. Exit")
    print()


def learn_today_opt(conn):
    print()
    print("#"*40)
    print("Learn today")
    print("#"*40)
    print()

    words_list = get_words_list_by_date(conn, date.today())
    start_learn_message(len(words_list))
    review_words_list(conn, words_list)
    end_learn_message()

    input("\nPress Enter to continue...")


def add_word_opt(conn):
    print()
    print("#"*40)
    print("Add new word")
    print("#"*40)
    print()

    word = input("Enter word: ").strip()

    if not word:
        print("Word cannot be empty.")
        input("\nPress Enter to continue...")
        return

    print(f'\nSearching for "{word}"...')

    result = lookup(word)

    if result is None:
        print(f'\nWord "{word}" was not found.')
        input("\nPress Enter to continue...")
        return

    print()
    print(result)

    choice = input("\nSave this word? [Y/n]: ").strip().lower()

    if choice in ("", "y", "yes"):
        review_status = default_review_status()
        if add_new_word(conn, result, review_status):
            print("\n✓ Word saved.")
        else:
            print("\nWord already exists.")

    input("\nPress Enter to continue...")


def vocabulary_opt(conn):
    print()
    print("#"*40)
    print("My vocabulary")
    print("#"*40)
    print()

    word_list = get_word_list(conn)
    print(f"Found {len(word_list)} word in vocabulary.")
    for w in word_list:
        print()
        show_word_info(w)
    input("\nPress Enter to continue...")


def search_word_opt():
    print()
    print("#"*40)
    print("Search word")
    print("#"*40)
    print()

    print("Not implemented yet.")
    input("\nPress Enter to continue...")


# Utilities function
def show_word_info(w: Word):
    print(w)
    # TODO: find better way to show word info instead of print all info of dataclass


def start_learn_message(word_count: int):
    print("Today's review")
    print("────────────────────────")
    print(f"{word_count} words to review")
    input("\nPress ENTER to start...")


def get_word_review_quality():
    print()
    print("""
        How well did you remember?

        [1] Again
        [2] Hard
        [3] Good
        [4] Easy
    """)
    q = int(input("\n>"))
    match q:
        case 1:
            return Quality.Again
        case 2:
            return Quality.Hard
        case 3:
            return Quality.Good
        case 4:
            return Quality.Easy
        case _:
            return None


def review_words_list(conn, words_list):
    word_count = len(words_list)
    for i in range(1, word_count + 1):
        w = words_list[i][0]
        r = words_list[i][1]

        print(f"Word {i}/{word_count}.")
        print()

        print(w.meaning)
        print("Guest which word ???")
        input("\nPress ENTER to show answer")

        show_word_info(w)
        q = get_word_review_quality()
        r.update(q)
        # TODO: update word review status on database instead of remove then add new one
        remove_word(conn, w.word)
        add_new_word(conn, w, r)


def end_learn_message():
    print("Learned all words. Congratulations")

def clear_screen():
    print("\033[2J\033[H", end="", flush=True)
