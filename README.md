English Spelling Game

Requirements:
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`

Usage:
1. Put your word lists in `word_folder/` as `KS1_words.txt`, `KS2_words.txt`, etc.
2. Run:
```
python EnglishGame.py
```

Notes:
- The program uses `gTTS` (requires internet) to pronounce words. If `gTTS` is unavailable, it will attempt an offline fallback using `pyttsx3`.
- A 20-second timer applies for typing each word.
