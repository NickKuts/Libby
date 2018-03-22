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
    l = []
    ll = sentence.split(' ', len(sentence))

    for i in range(0, len(ll) - 1):
        words = ll[i:i+2]

        word1 = ", ".join(words)
        word2 = ", ".join(reversed(words))

        l.append(word1)
        l.append(word2)

    return l + ll


def search_normal(sentence, fname='authors_clean.txt'):
    """
    Search through authors based on a sentence to see
    if the sentence contains an author's name (case ignored)
    """

    terms = generate_search_terms(sentence.lower())
    l = load_file(fname)

    for word in terms:
        ret = binary_search(l, word)

        if ret:
            return word

    return None


def search_closest(sentence, fname='authors_clean.txt'):
    """
    Search through authors based on a sentence to see
    if the sentence contains an author's name (case ignored)
    """

    terms = generate_search_terms(sentence.lower())
    l = load_file(fname)

    for word in terms:
        matches = get_close_matches(word, l, 1, 0.9)
        if len(matches) > 0:
            return matches[0]

    return None


def search(sentence, search_closest=True, fname='authors_clean.txt'):
    """
    Search through authors based on a sentence to see
    if the sentence contains an author's name (case ignored)
    :param sentence: the sentence where you wish to find a name
    :param search_closest: whether you want to also find the closest one
    if the exact name was not found
    """

    terms = generate_search_terms(sentence.lower())
    l = load_file(fname)

    for word in terms:
        res = binary_search(l, word)
        if res:
            return word

    # no exact match was found
    if search_closest:
        for word in terms:
            matches = get_close_matches(word, l, 1, 0.9)

            if len(matches) > 0:
                return matches[0]

    return None

