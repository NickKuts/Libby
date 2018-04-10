import json
import random
import string
from lambda_func.location_utils import ratio


with open('lambda_func/locations.json', 'r') as fp:
    locs = json.load(fp)


def rndm_str(k=20):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def existence(name):
    name = name.lower()

    res = []

    for loc in locs:
        location = locs[loc]
        aliases = location['aliases']
        for al in aliases:
            res.append((al, ratio(al.lower(), name)))

    return {name: res}


print_all_r = input('Print at all (Y/N)> ')
amount = int(input('Amount> '))


for i in range(0, amount):
    r = rndm_str()
    print(r)
    res = existence(r)

    count = 0
    avg = 0
    maxi = -1
    mini = 101
    highest = ''

    print_all = 'n'
    if print_all_r in 'Yy' and print_all_r != '':
        input("print all (Y/N> ")
    for ra in res[r]:
        if print_all.lower() in "Yy" and print_all != '': 
            print("\t{}".format(ra))
        curr = ra[1]
        count += 1
        avg += curr
        if curr > maxi:
            maxi = curr
            highest = ra[0]
        if curr < mini:
            mini = curr

    print("avg: {:.2f}, max: {}, min: {}, highest: {}".format(avg / count, maxi, mini, highest))
    print()

