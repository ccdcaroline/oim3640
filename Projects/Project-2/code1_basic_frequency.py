"""Code 1: Basic word-frequency analysis for song lyrics.

Requirements covered:
- Load text from a .txt file
- Count word frequencies using a dictionary
- Print top 10 most common words and basic stats
"""

from pathlib import Path


def load_text_from_txt(file_path: str) -> str:
    """Load and return raw text from a .txt file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def count_word_frequencies(text: str) -> dict[str, int]:
    """Count word frequencies using a dictionary (no advanced cleaning)."""
    word_counts: dict[str, int] = {}

    # Split on whitespace only for this basic version.
    words = text.split()
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1

    return word_counts


def print_top_words_and_stats(word_counts: dict[str, int], top_n: int = 10) -> None:
    """Print top-N words and basic stats."""
    total_words = sum(word_counts.values())
    unique_words = len(word_counts)

    print("=== BASIC LYRICS WORD ANALYSIS ===")
    print(f"Total words: {total_words}")
    print(f"Unique words: {unique_words}")
    print(f"Top {top_n} most common words:")

    sorted_items = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)
    for word, count in sorted_items[:top_n]:
        print(f"- {word}: {count}")


def main() -> None:
    """Load TXT lyrics and run basic analysis."""
    base_dir = Path(__file__).resolve().parent

    text_to_analyze = load_text_from_txt(
        str(base_dir / "data" / "taylor_sample_lyrics.txt")
    )

    counts = count_word_frequencies(text_to_analyze)
    print_top_words_and_stats(counts, top_n=10)


if __name__ == "__main__":
    main()
