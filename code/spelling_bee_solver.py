import os

# simple helpers

def uses_only(word, letters):
    """Return True if every character in word is one of the allowed letters."""
    for ch in word.lower():
        if ch not in letters:
            return False
    return True


def must_use(word, required):
    """Return True if required letter appears in word."""
    return required.lower() in word.lower()


def find_spelling_bee_words(letters, centre):
    """Find words that obey the Spelling Bee rules.

    letters: string with the seven allowed letters (case-insensitive)
    centre: the required letter (must be one of letters)
    """
    letters = letters.lower()
    centre = centre.lower()
    if centre not in letters:
        raise ValueError('centre letter not in the seven letters')

    # path to dictionary file
    base = os.path.dirname(__file__)
    dictfile = os.path.join(base, '..', 'data', 'words.txt')

    good = []
    with open(dictfile, encoding='utf-8') as f:
        for line in f:
            w = line.strip().lower()
            if len(w) < 4:
                continue
            if must_use(w, centre) and uses_only(w, letters):
                good.append(w)
    return good


if __name__ == '__main__':
    print('Enter the seven letters (no spaces): ')
    seven = input().strip().lower()
    print('Enter the centre letter: ')
    centre = input().strip().lower()
    words = find_spelling_bee_words(seven, centre)
    print('Found', len(words), 'words:')
    for w in words:
        print(w)


