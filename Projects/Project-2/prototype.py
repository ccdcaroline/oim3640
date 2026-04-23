"""Base scaffold for a Taylor Swift repetition analyzer.

This is a minimal starting file for a program that can later be
expanded with more lyric input, frequency analysis, repetition
patterns, and summary reporting.
"""

import re
from collections import Counter


def load_lyrics():
    """Return a small sample of song lyrics to analyze."""
    return {
        "Sample Song": (
            "I sing the same line again and again\n"
            "I sing the same line again and again\n"
            "Nothing really changes in this simple song"
        ),
    }


def normalize_text(text):
    """Normalize lyrics text for consistent analysis."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    return text


def count_words(text):
    """Count words in a song lyric string."""
    cleaned = normalize_text(text)
    words = cleaned.split()
    return Counter(words)


def analyze_song(title, lyrics):
    """Build a simple analysis result for one song."""
    counts = count_words(lyrics)
    total_words = sum(counts.values())
    unique_words = len(counts)

    return {
        "title": title,
        "total_words": total_words,
        "unique_words": unique_words,
        "word_counts": counts,
    }


# Future function to print a summary of results


def main():
    songs = load_lyrics()
    results = [analyze_song(title, lyrics) for title, lyrics in songs.items()]
    print_summary(results)



if __name__ == "__main__":
    main()
