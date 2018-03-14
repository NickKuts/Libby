from difflib import get_close_matches


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
        matches = get_close_matches(word, l, 1, 0.9)
        if len(matches) > 0:
            return matches[0]

    return "No author was found from sentence: " + sentence

