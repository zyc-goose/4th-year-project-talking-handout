# from jiwer import wer
from mywer import getWER, MyWER
from pageLayout import getRectArea

def getTextRecWER(pars, textrec):
    totalArea = sum(getRectArea(*x['coords']) for x in textrec)
    ret = MyWER()
    for par, x in zip(pars, textrec):
        frac = getRectArea(*x['coords']) / totalArea
        ret += frac * getWER(par['text'], x['text'])
    return ret
    