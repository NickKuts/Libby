import author_search as AS
import author_search_closest as ASC
import time


def normal(st):
    start = time.time()
    ret = AS.search(st)
    end = time.time()
    
    return (ret, (end - start) * 1000)

def closest(self):
    start = time.time()
    ret = ASC.search(st)
    end = time.time()

    return (ret,(end - start) * 1000)


st = 'the book was published by anttia roine in 1996'

n = normal(st)
print("Normal: " + n[0])
print("Normal time: " + str(n[1]))

c = closest(st)
print("Closest: " + c[0])
print("Closest time: " + str(c[1]))

