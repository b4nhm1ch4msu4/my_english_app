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

TODO:
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

### UI

#### Get user input

- add new word
- get today list words need to learn
- difficulty : easy/good/hard/again

#### Show output

- show options to choose : add new words/ learn today words
- show single word when learning to choose difficulty.


