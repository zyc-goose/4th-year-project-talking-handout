import json

pdir = '/Users/zyc/Documents/cam/courses/y4/project/source-code/output/'
paths = ['paragraphs.json', 'transcript.json']

for path in paths:
    with open(pdir + path) as fin:
        