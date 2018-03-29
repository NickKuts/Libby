import json


with open('locations.json', 'r') as fp:
    locations = json.load(fp)

addi = None
while not addi or not addi.strip() != '':
    addi = input('What do you want to add? ')

all_of = 'o'
while not (all_of in 'YyNn'):
    all_of = input('Do you want to skip those that already have {}? (Y/N)'.format(addi)) 

skip = all_of.lower() == 'y'

loop = True
for loc, data in locations.items():
    if loop:
        slot = data.get(addi, None)
        if not (skip and slot):
            print('---' * 30)
            print(data['aliases'])
            print('{}: {}'.format(addi, slot))
            print('building: {}'.format(data['building']))
            type_b = data['type']
            if type_b:
                print('type: {}'.format(type_b))
            add = 'o'
            while not add in 'YyNnCc':
                add = input('Do you want to add info? (C for cancel) (Y/N)')
            if add.lower() == 'y':
                n_addi = input('{}> '.format(addi))
                data[addi] = n_addi
            if add.lower() == 'c':
                loop = False
    else:
        n_data = data.get(addi, None)
        if not n_data or n_data == '':
            data[addi] = None


with open('locations.json', 'w') as fp:
    json.dump(locations, fp, indent=4)

