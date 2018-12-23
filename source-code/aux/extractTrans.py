"""
extractTrans.py

This script serves as an auxiliary function for manual transcription.

Since the transcription result produced by Google Cloud has very decent
accuracy, we can do manual transcription by modifying the existing
transcription result instead of starting from scratch, in order to 
save time.

The script takes 'output/transcript.json' as input and outputs the
extracted transcript (text only) into 'ground-truth/transcript.json'.
"""
import json

fin = open('../output/transcript.json')
fout = open('../ground-truth/transcript.json', 'w')

trans = json.load(fin)
output = []
buf = []
bufsize = 100

def add_newseg(output, buf):
    newseg = {}
    newseg['timestamp'] = 'mm:ss.xxx'
    newseg['text'] = ' '.join(buf)
    newseg['confidence'] = 0
    output.append(newseg)

for seg in trans:
    for word in seg['text'].split():
        if len(buf) == bufsize:
            add_newseg(output, buf)
            buf = []
        else:
            buf.append(word)
if len(buf) > 0:
    add_newseg(output, buf)
    buf = []

json.dump(output, fout, indent=4)

fin.close()
fout.close()