"""Code 3: Polished lyric repetition report.

Builds on Code 2 by adding:
- Clear presentation with formatted sections and table-like output
- Cleaner code structure for maintainability
"""

import csv
import string
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt

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


@dataclass
class AnalysisResult:
    """Container for final lyric analysis metrics."""

    total_raw_words: int
    total_cleaned_words: int
    unique_cleaned_words: int
    repetition_ratio: float
    most_repeated_word: str
    most_repeated_count: int
    top_words: list[tuple[str, int]]


def load_text(file_path: str, text_column: str = "lyrics") -> str:
    """Load text from .txt or .csv based on file extension."""
    path = Path(file_path)
    if path.suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8")

    if path.suffix.lower() == ".csv":
        lines = []
        with open(path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                value = row.get(text_column, "")
                if value:
                    lines.append(value)
        return "\n".join(lines)

    raise ValueError("Unsupported file format. Use .txt or .csv")


def tokenize_and_clean(text: str, stop_words: set[str]) -> tuple[list[str], list[str]]:
    """Return both raw and cleaned tokens for richer reporting."""
    raw_tokens = text.split()

    lowered = text.lower()
    translation_table = str.maketrans("", "", string.punctuation)
    no_punctuation = lowered.translate(translation_table)

    cleaned_tokens = [token for token in no_punctuation.split() if token not in stop_words]
    return raw_tokens, cleaned_tokens


def build_frequency_dict(tokens: list[str]) -> dict[str, int]:
    """Build frequency dictionary from a token list."""
    counts: dict[str, int] = {}
    for token in tokens:
        counts[token] = counts.get(token, 0) + 1
    return counts


def summarize_analysis(raw_tokens: list[str], cleaned_tokens: list[str]) -> AnalysisResult:
    """Compute summary statistics and top words."""
    word_counts = build_frequency_dict(cleaned_tokens)
    top_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:10]

    repeated_total = sum(count for count in word_counts.values() if count > 1)
    repetition_ratio = (repeated_total / len(cleaned_tokens)) if cleaned_tokens else 0.0

    if top_words:
        most_word, most_count = top_words[0]
    else:
        most_word, most_count = "", 0

    return AnalysisResult(
        total_raw_words=len(raw_tokens),
        total_cleaned_words=len(cleaned_tokens),
        unique_cleaned_words=len(word_counts),
        repetition_ratio=repetition_ratio,
        most_repeated_word=most_word,
        most_repeated_count=most_count,
        top_words=top_words,
    )


def print_report(result: AnalysisResult) -> None:
    """Print a polished, readable console report."""
    line = "=" * 66
    print(line)
    print("TAYLOR SWIFT LYRICS REPETITION REPORT")
    print(line)

    print("\nSUMMARY METRICS")
    print(f"- Raw word count:      {result.total_raw_words}")
    print(f"- Cleaned word count:  {result.total_cleaned_words}")
    print(f"- Unique cleaned words:{result.unique_cleaned_words:>4}")
    print(f"- Repetition ratio:    {result.repetition_ratio:.2%}")

    print("\nKEY QUESTIONS")
    print(
        f"1) Most repeated cleaned word: '{result.most_repeated_word}' "
        f"({result.most_repeated_count} times)"
    )
    print(
        "2) Overall repetitiveness: "
        f"{result.repetition_ratio:.2%} of cleaned words are repeated terms."
    )

    print("\nTOP 10 WORDS (TABLE)")
    print("+------+----------------------+-----------+")
    print("| Rank | Word                 | Frequency |")
    print("+------+----------------------+-----------+")
    for index, (word, count) in enumerate(result.top_words, start=1):
        print(f"| {index:<4} | {word:<20} | {count:>9} |")
    print("+------+----------------------+-----------+")


def save_bar_chart(top_words: list[tuple[str, int]], output_path: str) -> None:
    """Save a polished bar chart of top words."""
    words = [word for word, _ in top_words]
    counts = [count for _, count in top_words]

    plt.figure(figsize=(11, 6))
    plt.bar(words, counts)
    plt.title("Top Repeated Words in Sample Taylor Swift Lyrics", pad=12)
    plt.xlabel("Word")
    plt.ylabel("Frequency")
    plt.grid(axis="y", linestyle="--", alpha=0.35)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def run_pipeline(input_path: str, chart_path: str) -> None:
    """Run full polished analysis pipeline and present results."""
    text = load_text(input_path)
    raw_tokens, cleaned_tokens = tokenize_and_clean(text, STOP_WORDS)
    result = summarize_analysis(raw_tokens, cleaned_tokens)

    print_report(result)
    save_bar_chart(result.top_words, chart_path)
    print(f"\nChart saved to: {chart_path}")


def main() -> None:
    """Entry point for polished analysis."""
    base_dir = Path(__file__).resolve().parent
    input_file = str(base_dir / "data" / "taylor_sample_lyrics.txt")
    chart_file = str(base_dir / "top_words_code3.png")
    run_pipeline(input_file, chart_file)


if __name__ == "__main__":
    main()
