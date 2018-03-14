

def load_file(fname):
    """
    Load file and return it's contents as a list,
    split from new lines
    """
    l = []

    with open(fname, 'r') as f:
        lines = f.read()
        l = lines.split('\n', len(lines))

    return l


def binary_search(l, name):
    """
    Search the name from the list recursively. Return
    true if the name was found, false otherwise
    """

    half = int(len(l)/2)

    if half == 0:
        if l[half] == name:
            return True
        else:
            return False

    if l[half] > name:
        return binary_search(l[:half], name)
    elif l[half] < name:
        return binary_search(l[half:], name)
    elif l[half] == name:
        return True


def generate_search_terms(sentence):
    """
    Generate search terms from a sentence, that can
    be then searched from the list of authors.
    Also includes the names backwards, eg.
    Antti, Roine and Roine, Antti. The names are
    separated with a comma
    """

    l = sentence.split(' ', len(sentence))

    for i in range(0, len(l) - 1):
        words = l[i:i+2]

        word1 = ", ".join(words)
        word2 = ", ".join(reversed(words))

        l.append(word1)
        l.append(word2)
    
    return l


def search(sentence):
    """
    Search through authors based on a sentence to see
    if the sentence contains an author's name (case ignored)
    """

    terms = generate_search_terms(sentence.lower())
    l = load_file('authors_clean.txt')

    for word in terms:
        ret = binary_search(l, word)

        if ret:
            return word

    return "No authors was found from sentence: " + sentence

