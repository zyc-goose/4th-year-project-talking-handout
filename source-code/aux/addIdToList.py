import json

pdir = '/Users/zyc/Documents/cam/courses/y4/project/source-code/'
paths = ['output/paragraphs.json', 'output/transcript.json', 'ground-truth/textrec.json']

for path in paths:
    with open(pdir + path, 'r') as fin:
        obj = json.load(fin)
    for i, elem in enumerate(obj):
        elem['id'] = i
    with open(pdir + path, 'w') as fout:
        json.dump(obj, fout, indent=4)