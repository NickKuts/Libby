import json

filename = 'useful-aaltomap.json'


def test(f_p):
    aalto = json.load(f_p)
    for v in aalto['buildings']:
        if 'type' in v and v['type'] == 'restaurant':
            print('\t' + v['type'])
        if 'children' in v:
            child = v['children']
            for c in child:
                if 'type' in c and c['type'] == 'restaurant':
                    if 'name' in c:
                        print('name: ' + c['name'])
                    else:
                        print('id: ' + c['id'])
    print('###' * 30)
    for v in aalto['other']:
        if 'type' in v and v['type'] == 'restaurant':
            print('name: ' + v['name'])


with open(filename, 'r') as f:
    test(f)
