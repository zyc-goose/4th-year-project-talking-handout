import difflib
import re
from . import printMessage

def align(pars, trans):
    """Speech-Text alignment using diff.
    args:
        pars - list of extracted paragraphs
        trans - transcript of lecture audio
    returns:
        align_result - alignment result
    """
    # preprocess
    printMessage.begin('Preprocessing handout paragraphs and transcript')
    pars_words = []; pars_wordIDs = []
    for parID, par in enumerate(pars):
        words = re.sub(r'[^\w\d\s]', ' ', par['text']).lower().split()
        pars_words.extend(words)
        pars_wordIDs.extend([parID] * len(words))
    trans_words = []; trans_wordIDs = []
    for segID, seg in enumerate(trans):
        words = re.sub(r'[^\w\d\s]', ' ', seg['text']).lower().split()
        trans_words.extend(words)
        trans_wordIDs.extend([segID] * len(words))
    printMessage.end()
    
    # run diff
    printMessage.begin('Running alignment algorithm')
    diffs = difflib.ndiff(pars_words, trans_words)
    anchors = [None] * len(pars) # maps parID to segID
    anchors_matched_words = [None] * len(pars)
    parWID = segWID = -1; parWIDanc = segWIDanc = None
    consecutive = 0; consecutive_words = []
    for diff in diffs:
        if diff[0] == '-':
            parWID += 1
            consecutive = 0
            consecutive_words = []
        elif diff[0] == '+':
            segWID += 1
            consecutive = 0
            consecutive_words = []
        elif diff[0] == ' ': # match
            parWID += 1; segWID += 1
            if consecutive == 0:
                parWIDanc = parWID; segWIDanc = segWID
            consecutive += 1
            consecutive_words.append(diff[2:])
        if consecutive >= 2:
            parID = pars_wordIDs[parWID]
            segID = trans_wordIDs[segWID]
            anchors[parID] = segID
            anchors_matched_words[parID] = ' '.join(consecutive_words)
    printMessage.end()
    
    # generate result
    printMessage.begin('Generating alignment result')
    align_result = []
    for parID, segID in enumerate(anchors):
        match = {
            'parID': parID,
            'parText': pars[parID]['text'],
            'matchedAudioSegments': [],
            'matchedWords': ''
        }
        if segID is not None:
            match['matchedAudioSegments'].append({
                'segID': segID,
                'segTimeStamp': trans[segID]['timestamp'],
                'segText': trans[segID]['text']
            })
            match['matchedWords'] = anchors_matched_words[parID]
        align_result.append(match)
    printMessage.end()
    return align_result

