import json

a = {'1':'1',
     '2':'2'}

with open('1.json', 'w') as f:
    json.dump(a, f)