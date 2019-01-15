"""
Evaluation of the page layout analysis.
Two parameters:
    TPR: true positive rate
    TNR: true negative rate
"""

def getRectArea(x0, y0, x1, y1):
    return abs((x1 - x0) * (y1 - y0))

def getRectsIntersect(rectA, rectB):
    Ax0, Ay0, Ax1, Ay1 = rectA['coords']
    Bx0, By0, Bx1, By1 = rectB['coords']
    x0, y0 = max(Ax0, Bx0), max(Ay0, By0)
    x1, y1 = min(Ax1, Bx1), min(Ay1, By1)
    if x0 < x1 and y0 < y1:
        return getRectArea(x0, y0, x1, y1)
    return 0

def getResults(rects, trueRects, pdfImages):
    TP = FP = TN = FN = 0
    for img in pdfImages:
        TN += img.size[0] * img.size[1]
    for rect in rects:
        area = getRectArea(*rect['coords'])
        FP += area
        TN -= area
    for trueRect in trueRects:
        area = getRectArea(*trueRect['coords'])
        FN += area
        TN -= area
    for rect in rects:
        for trueRect in trueRects:
            if rect['page'] == trueRect['page']:
                area = getRectsIntersect(rect, trueRect)
                TP += area
                FP -= area
                FN -= area
                TN += area
    # Results
    TPR = TP / (TP + FN)
    TNR = TN / (TN + FP)
    return TPR, TNR

if __name__ == '__main__':
    print('test')
    print(getRectArea(1,2,3,5))
    rectA = {'coords': (3,1,15,10)}
    rectB = {'coords': (9,6,32,30)}
    print(getRectsIntersect(rectA, rectB))
    rectA = {'coords': (1,1,3,3)}
    rectB = {'coords': (4,5,6,6)}
    print(getRectsIntersect(rectA, rectB))