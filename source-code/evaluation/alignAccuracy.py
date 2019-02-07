def isGoodMatch(match, trueMatches):
    for trueMatch in trueMatches:
        if match['parID'] == trueMatch['parID'] and abs(match['segID'] - trueMatch['segID']) <= 1:
            return True
    return False

def getAlignAccuracy(matches, trueMatches):
    cnt = 0
    for match in matches:
        if isGoodMatch(match, trueMatches):
            cnt += 1
    return cnt / len(trueMatches)

def mapSegToMatch(seg):
    match = dict(
        parID=seg['parID'],
        segID=seg['matchedAudioSegments'][0]['segID'] if len(seg['matchedAudioSegments']) else -100
    )
    return match