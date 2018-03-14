from difflib import get_close_matches


steps = 0

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


def binary_search_half(l, name):
    """
    Search the name from the list recursively. Return
    true if the name was found, false otherwise
    """
    global steps
    steps += 1

    half = int(len(l)/2) 
    
    if half == 0:
        if l[half] == name:
            return [name]
        else:
            return []

    if steps > 4:
        return l

    if l[half] > name:
        return binary_search_half(l[:half], name)
    elif l[half] < name:
        return binary_search_half(l[half:], name)
    elif l[half] == name:
        return [name]


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
        smaller = binary_search_half(l, word)
        matches = get_close_matches(word, smaller, 1, 0.9)
        if len(matches) > 0:
            return matches[0]

    return "No author was found from sentence: " + sentence

