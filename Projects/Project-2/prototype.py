from pathlib import Path
 
def load_text(file_name="lyrics.txt"):
    file_path = Path(__file__).resolve().parent / file_name
    if not file_path.exists():
        raise FileNotFoundError(
            f"Could not find {file_name}. Put it here:\n{file_path}"
        )
    return file_path.read_text(encoding="utf-8")
 
def count_word_frequencies(text):
    words = text.split()  # basic split only
    freq = {}
 
    for word in words:
        if word in freq:
            freq[word] += 1
        else:
            freq[word] = 1
 
    return freq
 
def print_stats(freq):
    total_words = sum(freq.values())
    unique_words = len(freq)
 
    # sort by frequency (highest first)
    top_10 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
 
    print("=== BASIC ANALYSIS ===")
    print("Total words:", total_words)
    print("Unique words:", unique_words)
    print("Top 10 words:")
    for word, count in top_10:
        print(f"{word}: {count}")
 
def main():
    text = load_text("lyrics.txt")
    freq = count_word_frequencies(text)
    print_stats(freq)
 
if __name__ == "__main__":
    main()
