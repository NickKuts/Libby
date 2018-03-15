import author_search_combined as AS
import time


def normal(st):
    start = time.time()
    ret = AS.search_normal(st)
    end = time.time()
    
    return (ret, (end - start) * 1000)

def closest(self):
    start = time.time()
    ret = AS.search_closest(st)
    end = time.time()

    return (ret,(end - start) * 1000)


def combined(self):
    start = time.time()
    ret = AS.search_combined(st)
    end = time.time()

    return (ret,(end - start) * 1000)


st = 'im looking for a book by antti roine from ninety six srpökö'

n = normal(st)
print("Normal: " + n[0])
print("Normal time: " + str(n[1]))

c = closest(st)
print("Closest: " + c[0])
print("Closest time: " + str(c[1]))

cc = combined(st)
print("Combined: " + cc[0])
print("Combined time: " + str(cc[1]))
