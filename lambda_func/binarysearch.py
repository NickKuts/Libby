import time

ll = []

def load_file(fname):
    lista = []

    with open(fname, 'r') as f:
        lines = f.read()
        lista = lines.split('\n', len(lines))
    
    return lista

i = 0

def binary_search(l, name):
    
    half = int(len(l)/2)
    
    global i
    i += 1

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
    l = []
    
    l = sentence.split(' ', len(sentence))

    for i in range(0, len(l) - 2):
        words = l[i:i+2]
        
        word = ", ".join(words)
        word2 = ", ".join(reversed(words))
        l.append(word)
        l.append(word2)
    
    return l


def search(sentence):
   
    terms = generate_search_terms(sentence)
       
    global ll
    
    for word in terms:
        ret = binary_search(ll, word)
        print(word)
        if ret:
            return word

    return "Not found"


ll = load_file('authors.txt')
ll = list(set(ll))
ll.sort()

name = 'Roine, Antti'

sentence = 'find book cats written by Antti Roine from the year 1991'

ret = search(sentence)
print("ll length:", len(ll))

print("Found name", name, ":", ret)
print("iterations:",i)

