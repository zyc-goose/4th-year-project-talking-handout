"""
output/paragraphs.json -> output/pageseg.json
"""

import json, os
from uuid import uuid4

with open(os.path.dirname(__file__) + '/config.json', 'r') as cfgfile:
    config = json.load(cfgfile)

# Page Layout Analysis
def mapParToRect(par):
    l, t, w, h = par['left'], par['top'], par['width'], par['height']
    rect = dict(
        id = str(uuid4()),
        page=par['pageNum'],
        coords=(l, t, l+w, t+h),
        selected=False
    )
    return rect

with open(config['OCRParsPath'], 'r') as fin, open(config['rectPath'], 'w') as fout:
    pars = json.load(fin)
    rects = list(map(mapParToRect, pars))
    json.dump(rects, fout, indent=4)