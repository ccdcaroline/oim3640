"""Code 2: Cleaner analysis with questions and visualization.

Builds on Code 1 by adding:
- Text cleaning (lowercase, punctuation removal, stop-word removal)
- Answers to at least 2 interesting analysis questions
- One visualization (bar chart)
- Well-named functions
"""

import string
from pathlib import Path

import matplotlib.pyplot as plt

# A compact custom stop-word set for this project.
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "got",
    "hi",
    "i",
    "im",
    "in",
    "is",
    "it",
    "its",
    "me",
    "my",
    "now",
    "of",
    "off",
    "on",
    "or",
    "the",
    "to",
    "up",
    "we",
    "were",
    "what",
    "when",
    "with",
    "you",
    "your",
    "know",
    "dont",
    "about",
    "cause",
    "gonna",
}


def load_text_from_txt(file_path: str) -> str:
    """Load and return raw text from a txt file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def clean_text(text: str) -> list[str]:
    """Lowercase text, remove punctuation, and filter stop words."""
    lowered = text.lower()
    translation_table = str.maketrans("", "", string.punctuation)
    no_punctuation = lowered.translate(translation_table)

    tokens = no_punctuation.split()
    cleaned_tokens = [token for token in tokens if token not in STOP_WORDS]
    return cleaned_tokens


def count_word_frequencies(tokens: list[str]) -> dict[str, int]:
    """Count token frequencies with a dictionary."""
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts


def get_top_n_words(word_counts: dict[str, int], n: int = 10) -> list[tuple[str, int]]:
    """Return top-N words sorted by count descending."""
    return sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:n]


def calculate_repetition_ratio(tokens: list[str], word_counts: dict[str, int]) -> float:
    """Compute repetition ratio = repeated words / total words."""
    repeated_count = sum(count for count in word_counts.values() if count > 1)
    total_count = len(tokens)
    if total_count == 0:
        return 0.0
    return repeated_count / total_count


def find_most_repeated_word(word_counts: dict[str, int]) -> tuple[str, int]:
    """Find the single most repeated word and its count."""
    if not word_counts:
        return "", 0
    return max(word_counts.items(), key=lambda item: item[1])


def answer_analysis_questions(tokens: list[str], word_counts: dict[str, int]) -> None:
    """Answer at least two interesting questions about lyric repetition."""
    top_word, top_count = find_most_repeated_word(word_counts)
    repetition_ratio = calculate_repetition_ratio(tokens, word_counts)

    print("\n=== QUESTION-DRIVEN INSIGHTS ===")
    print("Q1) What word is repeated the most?")
    print(f"A1) '{top_word}' appears {top_count} times.")

    print("\nQ2) How repetitive are these lyrics overall?")
    print(
        "A2) Repetition ratio "
        f"(words occurring >1 time / all cleaned words) = {repetition_ratio:.2%}."
    )


def plot_top_words(top_words: list[tuple[str, int]], output_path: str) -> None:
    """Create and save a bar chart of top words."""
    words = [item[0] for item in top_words]
    counts = [item[1] for item in top_words]

    plt.figure(figsize=(10, 5))
    plt.bar(words, counts)
    plt.title("Top 10 Most Common Cleaned Words in Sample Taylor Swift Lyrics")
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def run_analysis(text: str, chart_path: str) -> None:
    """Run the full cleaned analysis workflow."""
    tokens = clean_text(text)
    word_counts = count_word_frequencies(tokens)
    top_words = get_top_n_words(word_counts, n=10)

    print("=== CLEANED LYRICS ANALYSIS ===")
    print(f"Cleaned word count: {len(tokens)}")
    print(f"Unique cleaned words: {len(word_counts)}")
    print("Top 10 cleaned words:")
    for word, count in top_words:
        print(f"- {word}: {count}")

    answer_analysis_questions(tokens, word_counts)
    plot_top_words(top_words, chart_path)
    print(f"\nSaved bar chart to: {chart_path}")


def main() -> None:
    """Load TXT sample data and run Code 2 analysis."""
    base_dir = Path(__file__).resolve().parent
    text = load_text_from_txt(str(base_dir / "data" / "taylor_sample_lyrics.txt"))

    chart_output = str(base_dir / "top_words_code2.png")
    run_analysis(text, chart_output)


if __name__ == "__main__":
    main()
