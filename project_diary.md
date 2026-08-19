# Project Diary

Week	Goal
1	    Build a word search UI and fetch dictionary data
2	    Save words into SQLite
3	    Implement the review mechanism
4	    Implement UI
5	    Improve the UI, handle edge cases, and package a usable release
6	    Let friends use it and gather feedback

## Week 1: Build a word search UI and fetch dictionary data

## Week 2: Save words into SQLite

- [x] Build word model
- [x] Create database
- [x] Insert new word to database
- [x] View word list
- [x] Remove a word
- [x] Get a word from list
- [x] add test cases
- [x] add logging system

## Week 3: Implement the review mechanism

### The SuperMemo-2(SM-2) Algorithm

- Which words need to learn today?
- When should re-learn this word ?

- [x] Create SM-2 algo
- [x] Create review status
- [x] How to save learning info to a single word ?
- [x] Modify add new word method to add review status to database
- [x] database init method (add review status)
- [x] database add get review status method
- [x] Get today words list
- [x] Add test unit to test get review status from database
- [x] Fix get_word bug when return 


## Week 4: Implement UI

### TUI files layer

app/
├── main.py
├── models.py
├── database.py
├── dictionary.py
├── scheduler.py
├── logger.py
│
└── tui/
    ├── __init__.py
    ├── menu.py
    ├── review.py
    ├── vocabulary.py
    └── search.py

### Main UI
```
╔══════════════════════════════════════╗
║          English Learning            ║
╠══════════════════════════════════════╣
║                                      ║
║  1. Learn today                      ║
║  2. Add new word                     ║
║  3. My vocabulary                    ║
║  4. Search word                      ║
║  5. Delete word                      ║
║  6. Exit                             ║
║                                      ║
╚══════════════════════════════════════╝

Choose an option:
```

TODO:
- [x] 1. Learn today
- [x] 2. Add new word
- [x] 3. My vocabulary
- [ ] 4. Search word
- [ ] 5. Delete word
- [ ] 6. Exit

#### 1. Learn today

##### start message (done)

```
Today's review
────────────────────────

5 words to review

Press ENTER to start...
```

##### review card

```
┌──────────────────────────────────────┐
│              Card 1 / 5              │
├──────────────────────────────────────┤
│                                      │
│              abandon                 │
│                                      │
│          What does it mean?          │
│                                      │
│                                      │
│         [ENTER] Show answer          │
│                                      │
└──────────────────────────────────────┘
```

##### show answer

```
┌──────────────────────────────────────┐
│              Card 1 / 5              │
├──────────────────────────────────────┤
│                                      │
│              abandon                 │
│                                      │
│           /əˈbændən/                 │
│                                      │
│  verb                                │
│                                      │
│  To leave someone or something       │
│  permanently.                        │
│                                      │
│  Example:                            │
│  He abandoned the project.           │
│                                      │
└──────────────────────────────────────┘

How well did you remember?

[1] Again
[2] Hard
[3] Good
[4] Easy
```

##### update after rating

```
✓ Good

Next review:
in 6 days

Press ENTER for next word...
```

##### ending message

```
╔══════════════════════════════════════╗
║          Review Complete!            ║
╠══════════════════════════════════════╣
║                                      ║
║  Reviewed:       5                   ║
║  Again:          1                   ║
║  Hard:           1                   ║
║  Good:           2                   ║
║  Easy:           1                   ║
║                                      ║
║  🎉 Great job!                       ║
║                                      ║
╚══════════════════════════════════════╝

Press ENTER to return to menu...
```

#### 2. Add new word

##### input new word

```
Enter word:

>
```

##### after searching word

```
Found:

abandon
/əˈbændən/

verb

To leave someone or something permanently.

Example:
He abandoned the project.
```

```
Save this word?

[Y] Yes
[N] No
```

```
✓ Word saved.

It will be available for today's learning.
```

```
Word not found.

Press ENTER to try another word...
```

```
"abandon" is already in your vocabulary.

[1] View word
[2] Return to menu
```

#### 3. My vocabulary (optional)

```
╔══════════════════════════════════════╗
║             My Vocabulary            ║
╠══════════════════════════════════════╣
║                                      ║
║  1. abandon                          ║
║  2. achieve                          ║
║  3. implement                        ║
║  4. reluctant                        ║
║  5. subtle                           ║
║                                      ║
╚══════════════════════════════════════╝

Enter word number:
```

```
implement
──────────────────────────────────────

/ˈɪmplɪment/

verb

To put a plan or decision into effect.

Example:
We need to implement the new system.

Review:
──────────────────────────────────────
Reviews:       4
Interval:      7 days
Next review:   Aug 25, 2026

[1] Delete
[2] Back
```

#### 4. Search word (optional)

```
Search:

> ephemeral

Searching...
```

```
ephemeral

/ɪˈfemərəl/

adjective

Lasting for a very short time.

Example:
Fame can be ephemeral.

Not saved.

[1] Save to vocabulary
[2] Search another
[3] Back
```

#### 5. Delete word (not implement yet)

#### 6. Exit

### overview
```
                    ┌─────────────┐
                    │ Main Menu   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     Learn Today       Add Word        Vocabulary
          │                │                │
          ▼                ▼                ▼
       Review          Dictionary       Word Detail
          │                │                │
          ▼                ▼                ▼
      Complete          Save/Delete       Back
          │
          └───────────────┐
                          ▼
                     Main Menu
```

