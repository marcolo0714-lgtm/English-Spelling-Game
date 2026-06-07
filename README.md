# English Spelling Game

A simple English spelling practice game built with Python and Pygame.

## Overview

`EnglishGame.py` presents a graphical spelling challenge where players hear a word, type it in, and receive instant feedback.

The game includes:
- word lists for 4 difficulty levels (`KS1` to `KS4`)
- optional audio pronunciation with `gTTS` and `pygame`
- keyboard and mouse controls with on-screen guidance

## Requirements

- Python 3.8+
- `pygame`
- `gTTS`
- `pandas`
- `requests`
- `openpyxl`

Install dependencies with:

```bash
pip install -r requirements.txt
```

> If you only want to run the game and not the helper scripts, `pygame` and `gTTS` are the main runtime dependencies.

## Installation

From the project folder:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Then run the game:

```bash
python EnglishGame.py
```

## Running the Game

- Launch the game from the project root
- Select a KS level to load the corresponding word list
- Click `Next` or press `Space` to start a round
- Type the word and press `Enter` to submit
- Use `Rehear` or `Up` to hear the word again
- Use `Reset score` or `Down` to reset the current score
- Use `Left` / `Right` to change levels when no round is active
- Press `Esc` or click `Exit` to quit

## Video Showcase

https://github.com/user-attachments/assets/630f17a2-54d2-48f8-9967-20cff1207d90



## Directory Structure

- `requirements.txt` — Python dependency list
- `EnglishGame.py` — main game script
- `wordlist_KS1-4.xlsx` — source Excel file used by helper scripts
- `app.log` — log file produced by helper scripts
- `key_button_image/` — image assets for on-screen key hints
- `word_folder/`
  - `KS1_words.json` through `KS4_words.json` — game word data used at runtime.
  - `excel_2_json.py` — helper to import custom words from `word_folder/custom_wordlist.xlsx`. The Excel file includes all vocabularies from EDB official wordlist, with AI-generated part of speech, meaning, and manually added alternative spellings.
- `word_folder2 (API)/`
  - `KS1_words.json` through `KS4_words.json` — API-generated word data. It is currently not used for the game.
  - `excel_2_json.py` — helper that fetches definitions from dictionaryapi.dev

## Notes

- The game loads word data from JSON files under `word_folder/`.
- `gTTS` requires an Internet connection to generate speech. If unavailable, the game will still run but pronunciation will be disabled.
- The helper scripts use `pandas`, `requests`, and `openpyxl` to process Excel files and fetch definitions.
- Update the `word_folder/*_words.json` files directly or use the helper scripts to add or refresh vocabulary.

## Attribution

- The word list in this directory, `wordlist_KS1-4.xlsx`, is downloaded from the official Education Bureau website: https://www.edb.gov.hk/en/curriculum-development/kla/eng-edu/references-resources/Enhancing%20Eng%20Vocab%20at%20Sec%20Level.html
- The image assets in `key_button_image/` are made by shohanur.rahman13 from www.flaticon.com: https://www.flaticon.com/packs/keyboard-buttons-3?word=keyboard%20button
