import json, os
import pdf2image as p2i
import pageLayout as pla
from jiwer import wer

with open(os.path.dirname(__file__) + '/config.json', 'r') as cfgfile:
    config = json.load(cfgfile)

# Page Layout Analysis
with open(config['trueRectsPath']) as trin, open(config['rectsPath']) as rin:
    rects = json.load(rin)
    trueRects = json.load(trin)
    pdfImages = p2i.convert_from_path(config['pdfPath'])
    TPR, TNR = pla.getResults(rects, trueRects, pdfImages)
    print('TPR =', TPR)
    print('TNR =', TNR)

# Speech Recogniser WER
with open(config['transPath']) as tin, open(config['trueTransPath']) as ttin:
    trans = json.load(tin)
    trueTrans = json.load(ttin)
    transText = ' '.join(map(lambda x: x['text'], trans))
    trueTransText = ' '.join(map(lambda x: x['text'], trueTrans))
    print('WER (SR) =', wer(trueTransText, transText, standardize=True))