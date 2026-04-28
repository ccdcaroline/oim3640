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
 
 
def parse_songs(text):
    """
    Expects format:
    === SONG: Song Name ===
    lyric lines...
    """
    songs = {}
    current_title = None
    current_lines = []
 
    for raw_line in text.splitlines():
        line = raw_line.strip()
 
        if line.startswith("=== SONG:") and line.endswith("==="):
            # Save previous song before starting a new one
            if current_title is not None:
                songs[current_title] = " ".join(current_lines).strip()
 
            # Extract title
            title = line.replace("=== SONG:", "").replace("===", "").strip()
            current_title = title
            current_lines = []
        else:
            if line:  # ignore empty lines
                current_lines.append(line)
 
    # Save last song
    if current_title is not None:
        songs[current_title] = " ".join(current_lines).strip()
 
    return songs
 
 
def clean_words(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    return [w for w in words if w not in STOP_WORDS]
 
 
def make_frequency_dict(words):
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq
 
 
def analyze_song(song_title, song_text):
    words = clean_words(song_text)
    freq = make_frequency_dict(words)
 
    total = len(words)
    unique = len(freq)
    repetition_percent = ((total - unique) / total) * 100 if total else 0.0
 
    if freq:
        top_word, top_count = max(freq.items(), key=lambda x: x[1])
    else:
        top_word, top_count = "", 0
 
    top5 = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
 
    return {
        "title": song_title,
        "total_words": total,
        "unique_words": unique,
        "repetition_percent": repetition_percent,
        "top_word": top_word,
        "top_count": top_count,
        "top5": top5,
    }
 
 
def print_comparison_table(results):
    print("=" * 92)
    print("THREE-SONG REPETITION COMPARISON")
    print("=" * 92)
    print(f"{'Song':<20}{'Total':>8}{'Unique':>10}{'Repeat %':>12}{'Top Word':>18}{'Count':>10}")
    print("-" * 92)
 
    for r in results:
        print(
            f"{r['title'][:20]:<20}"
            f"{r['total_words']:>8}"
            f"{r['unique_words']:>10}"
            f"{r['repetition_percent']:>11.2f}%"
            f"{r['top_word'][:16]:>18}"
            f"{r['top_count']:>10}"
        )
 
    print("-" * 92)
    print("\nTop 5 words by song:")
    for r in results:
        print(f"\n{r['title']}:")
        for word, count in r["top5"]:
            print(f"  {word}: {count}")
 
 
def plot_repetition_comparison(results):
    titles = [r["title"] for r in results]
    repetition_values = [r["repetition_percent"] for r in results]
 
    plt.figure(figsize=(9, 5))
    bars = plt.bar(titles, repetition_values)
    plt.title("Repetition % Comparison Across 3 Songs")
    plt.xlabel("Song")
    plt.ylabel("Repetition %")
    plt.ylim(0, max(repetition_values) + 10 if repetition_values else 100)
 
    for bar, value in zip(bars, repetition_values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{value:.1f}%",
            ha="center"
        )
 
    plt.tight_layout()
    plt.savefig("three_song_repetition_comparison.png")
    plt.show()
 
 
def main():
    text = load_text("lyrics.txt")
    songs = parse_songs(text)
 
    if len(songs) != 3:
        print(f"Found {len(songs)} songs. This script is designed for 3 songs.")
        print("Make sure your file has three headers like: === SONG: Name ===")
        return
 
    results = []
    for title, song_text in songs.items():
        results.append(analyze_song(title, song_text))
 
    print_comparison_table(results)
    plot_repetition_comparison(results)
 
 
if __name__ == "__main__":
    main()