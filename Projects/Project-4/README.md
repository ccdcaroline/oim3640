# Project 4: Taylor Swift Lyrics Repetition Analysis

This project contains **3 progressive Python code versions** that build toward a complete lyric repetition analyzer.

## Files

- `code1_basic_frequency.py`
  - Loads text from `.txt`, `.csv`, or a pasted string
  - Counts word frequency with a dictionary
  - Prints top 10 words + basic stats

- `code2_cleaned_analysis.py`
  - Adds cleaning (lowercase, punctuation removal, stop-word removal)
  - Answers 2 analysis questions
  - Creates a bar chart (`top_words_code2.png`)
  - Uses organized, well-named functions

- `code3_polished_report.py`
  - Adds cleaner structure and polished presentation
  - Prints formatted report + table
  - Saves polished bar chart (`top_words_code3.png`)

## Data

Sample lyric data is in:
- `data/taylor_sample_lyrics.txt`
- `data/taylor_sample_lyrics.csv`

## Run

From this folder (`Projects/Project-4`):

```bash
python3 code1_basic_frequency.py
python3 code2_cleaned_analysis.py
python3 code3_polished_report.py
```

## Dependency

Code 2 and 3 require matplotlib:

```bash
python3 -m pip install matplotlib
```
