
import json
import re


file_name = 'sample_utterances.json'

with open(file_name, 'r') as fp:
    samps = json.load(fp)

re_patt = r'(?P<location>.+)'

for i in range(0, len(samps)):
    samps[i] = re.compile(samps[i].replace('{place}', re_patt))

inp = input('> ')

while inp != '':
    matches = []
    for samp in samps:
        t = samp.fullmatch(inp)
        if t:
            try:
                matches.append((samp, t.group('location')))
            except: pass

    matches.sort(key=lambda x: len(x[1]), reverse=True)
    longest = None
    if len(matches) > 0:
        longest = matches[0][1]
        for reg in matches:
            m = reg[0].fullmatch(longest)
            if m:
                try:
                    longest = m.group('location')
                except: pass

    print(longest)

    inp = input('> ')

"""
while inp != '':
    for samp in samps:
        try:
            print(samp.split(inp))
            print(samp)
        except:
            pass
    inp = input('> ')

while inp != '':
    for samp in samps:
        if samp.match(inp):
            print(samp)
    inp = input('> ')
"""
