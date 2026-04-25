from pathlib import Path 
import string
import matplotlib.pyplot as plt
 
STOP_WORDS = {
    "the", "and", "a", "an", "to", "of", "in", "is", "it", "i", "you", "me",
    "my", "we", "are", "was", "were", "be", "on", "for", "with", "that", "this"
}
 
def load_text(file_name="lyrics.txt"):
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / file_name   # same folder as polished.py
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
 
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    cleaned_words = [w for w in words if w not in STOP_WORDS]
    return cleaned_words
 
def count_word_frequencies(words):
    freq = {}
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
    return freq
 
def top_words(freq, n=10):
    return sorted(freq.items(), key=lambda x: x[1], reverse=True)[:n]
 
def answer_questions(words, freq):
    total_words = len(words)
    unique_words = len(freq)
 
    most_word, most_count = max(freq.items(), key=lambda x: x[1])
 
    # question 2: how repetitive?
    # repeated share = (total - unique) / total
    repetition_percent = ((total_words - unique_words) / total_words) * 100 if total_words else 0
 
    print("\n=== QUESTIONS ===")
    print(f"1) Most repeated word: '{most_word}' ({most_count} times)")
    print(f"2) Repetition percentage: {repetition_percent:.2f}%")
 
def make_bar_chart(top10):
    words = [w for w, c in top10]
    counts = [c for w, c in top10]
 
    plt.figure(figsize=(9, 5))
    plt.bar(words, counts)
    plt.title("Top 10 Most Common Words")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("top_words_code2.png")
    plt.show()
 
def main():
    text = load_text("lyrics.txt")
    words = clean_text(text)
    freq = count_word_frequencies(words)
    top10 = top_words(freq, 10)
 
    print("=== CLEANED ANALYSIS ===")
    print("Cleaned word count:", len(words))
    print("Unique cleaned words:", len(freq))
    print("Top 10 words:")
    for word, count in top10:
        print(f"{word}: {count}")
 
    answer_questions(words, freq)
    make_bar_chart(top10)
 
if __name__ == "__main__":
    main()