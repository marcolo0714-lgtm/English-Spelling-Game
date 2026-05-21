# English Spelling Game

A simple English spelling practice game built with Python and Pygame.

## Overview

`EnglishGame.py` presents a graphical spelling challenge where players hear a word, type it in, and receive instant feedback.

The game includes:
- word lists from 4 difficulty levels (`KS1` to `KS4`) according to the Education Bureau
- audio pronunciation using `gTTS` when available (connection to the Internet required)
- keyboard and mouse controls with on-screen guidance

## Requirements

- Python 3.8+
- `pygame`
- `gtts`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the Game

From the project folder, run:

```bash
python EnglishGame.py
```

## Controls

- Click a level button (`KS1`–`KS4`) to choose the difficulty level and load that word list
- Press `Space` or click `Next` to start a round and hear the word
- Type the word into the input box when the round starts
- Press `Enter` to submit your answer
- Click `Rehear` or press `Up` to hear the word again
- Click `Reset score` or press `Down` to reset the score for the current level
- Use `Left` / `Right` arrows to change the selected level when a round is not active
- Press `Esc` or click `Exit` to quit the game

## Video Showcase

https://github.com/user-attachments/assets/9d657128-cff1-401c-b54b-e66ad1620968


## Directory Structure

- `requirements.txt` — Python dependency list
- `EnglishGame.py` — main game script
- `excel_2_text.py` — helper function to read the excel from the Education Bureau (see attributions) to the text files in `word_folder/`
- `word_folder/` — text files containing level-specific words
- `key_button_image/` — image assets for on-screen control hints

## Notes

- The difficulty of words in this game is determined by the Key-Stage (KS) level as mentioned by the Education Bureau. According to the Education Bureau, Hong Kong students are expected to know about:
  - 1,000 words by KS1 (P1 - P3), 
  - 2,000 words by KS2 (P4 - P6), 
  - 3,500 words by KS3 (S1 - S3), and 
  - 5,000 words by KS4 (S4 - S6).
- If `gTTS` is unavailable, word pronunciation does not work, and the game is unplayable.
- The game uses a 20-second timer for each spelling round.
- Add or update words in the `word_folder` text files (one word per line) to customize the vocabulary.

## Attribution

- The word list in this directory, `wordlist_KS1-4.xlsx`, is downloaded from the official Education Bureau website: https://www.edb.gov.hk/en/curriculum-development/kla/eng-edu/references-resources/Enhancing%20Eng%20Vocab%20at%20Sec%20Level.html 
- The image assets in `key_button_image/` are made by shohanur.rahman13 from www.flaticon.com: https://www.flaticon.com/packs/keyboard-buttons-3?word=keyboard%20button 
