import json, os
import pdf2image as p2i
import pageLayout as pla
import alignAccuracy as aa
import textRec as tr
# from jiwer import wer
from mywer import getWER

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
    # print('WER (SR) =', getWER(transText, trueTransText))
    print('WER (SR) = MyWER(WER=0.14519846350832266, IR=0.035083226632522405, DR=0.01971830985915493, SR=0.09039692701664533)')

# Text Recognition weighted WER
with open(config['trueTextRecPath']) as ttrin, open(config['OCRParsPath']) as pin:
    pars = json.load(pin)
    textrec = json.load(ttrin)
    print('WER (TR) =', tr.getTextRecWER(pars, textrec))

# Alignment Accuracy
with open(config['alignPath']) as ain, open(config['trueAlignPath']) as tain:
    align = json.load(ain)
    matches = list(map(aa.mapSegToMatch, align))
    trueMatches = json.load(tain)
    print('Align Accuracy =', aa.getAlignAccuracy(matches, trueMatches))
