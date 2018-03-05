#!/usr/bin/env python3.6

from main_handler import lambda_handler
import json

with open("restaurants.json", "r") as fp:
    rests = json.load(fp).keys()

print("Choose one, alvari is default:")
inp = input("Print all possibilities? (Y/n): ")
if inp == 'Y':
    for r in rests:
        print(r)
inp = input("> ")

if inp == '':
    inp = 'alvari'

rest = inp

fi = json.load(open("location.json"))

fi['currentIntent']['slots']['place'] = rest

a = lambda_handler(fi, 1234567)

print(a)

