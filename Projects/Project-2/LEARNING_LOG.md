## Date: April 24, 2026 

**What I asked AI to do:**
- Generate a Python program that reads a text file and analyzes it by counting how often each word appears, then prints basic statistics.

**What I didn’t understand in the generated code:**
- The line using Path(__file__).resolve().parent / file_name was confusing. I didn’t know how it builds the file path or what __file__ refers to.
- I also didn’t fully understand if __name__ == "__main__": and why main() is inside that condition.
- The sorted(freq.items(), key=lambda x: x[1], reverse=True) part was a little confusing, especially the lambda function and how it sorts by values instead of keys.

**What I learned:**
- Path(__file__) refers to the current Python file, and .parent / file_name builds a path to another file in the same folder. This is a safer way to locate files.
- The if __name__ == "__main__": line makes sure the main() function only runs when the file is executed directly, not when it’s imported into another file.
- freq.items() turns the dictionary into pairs like (word, count), and the lambda x: x[1] tells Python to sort based on the count (the second value in each pair).
- The dictionary freq is used to count words by checking if a word already exists and updating the count

## Date: April 24, 2026 

**What I asked AI to do:** 
- Improve my Project 2 code so it cleans the lyrics, removes common words, counts the most repeated words, answers basic questions, and makes a bar chart. 

**What I didn't understand in the AI code:** 
- The cleaned_words = [w for w in words if w not in STOP_WORDS] line was confusing because it is a shorter way to write a loop.
- I also didn’t fully understand how matplotlib creates and saves the bar chart.

**What I learnd:** 
- Cleaning text makes the analysis better because it removes punctuation, capital letters, and basic words like “the” or “and.”
- A list comprehension is a shorter way to make a new list from an old list.
- matplotlib can turn the top word counts into a visual bar chart.
- Splitting the project into functions makes the code easier to understand and update.






