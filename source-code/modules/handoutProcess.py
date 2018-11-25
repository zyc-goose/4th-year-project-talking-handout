import pytesseract
import pdf2image
from . import printMessage
import os
import re
import json
from PIL import Image
from collections import namedtuple

def pdf_to_images(abspath):
    """Convert a single PDF file to a list of PIL images.
    args:
        abspath - absolute path of the PDF file
    returns:
        images - list of converted PIL images
    """
    filename = os.path.basename(abspath)
    printMessage.begin("Converting '%s' to PIL images" % filename)
    images = pdf2image.convert_from_path(abspath)
    printMessage.end()
    return images


def images_to_obj(images):
    """Process the PIL images by OCR engine and store results in a dict.
    args:
        images - PIL images converted from PDF file
    returns:
        obj - a Python dict which stores all processing results from OCR
    """
    
    obj = {
        'totalPages': len(images), 
        'pages': []
    }
    for k, image in enumerate(images):
        printMessage.begin('Processing PIL images [%d/%d]' % (k+1, len(images)))
        tsvdata = pytesseract.image_to_data(image)
        lines = tsvdata.split('\n')
        BBox = namedtuple('BBox', lines[0])
        page_bbox = BBox(*map(int, lines[1].split()), None)
        page = {
            'pageNum': k + 1, 
            'width': page_bbox.width, 
            'height': page_bbox.height,
            'blocks': []
        }
        obj['pages'].append(page)
        for line in lines[2:]:
            line_splitted = line.split()
            bbox = BBox(*map(int, line_splitted[:11]), None)
            bbox_pos = {
                'left': bbox.left,
                'top': bbox.top,
                'width': bbox.width,
                'height': bbox.height
            }
            if bbox.level == 2: # block
                block = {
                    'blockNum': len(page['blocks']) + 1,
                    **bbox_pos,
                    'pars': []
                }
                page['blocks'].append(block)
            elif bbox.level == 3: # paragraph
                par = {
                    'parNum': len(block['pars']) + 1,
                    **bbox_pos,
                    'words': []
                }
                block['pars'].append(par)
            elif bbox.level == 5: # word
                word = {
                    'wordNum': len(par['words']) + 1,
                    **bbox_pos,
                    'confidence': bbox.conf,
                    'text': line_splitted[-1]
                }
                par['words'].append(word)
    printMessage.end()
    return obj


def obj_to_pars(obj, reject_thres=75):
    """Convert OCR results (obj) to a list of paragraphs.
    args:
        obj - Python dict which stores all processing results from OCR
        reject_thres - rejection threshold for words based on confidence scores
    returns:
        pars - a list of paragraph objects
    """
    pars = []
    printMessage.begin('Converting OCR results to list of paragraphs (rejection threshold %d)' % reject_thres)
    for page in obj['pages']:
        for block in page['blocks']:
            for par in block['pars']:
                words = []
                for word in par['words']:
                    if word['confidence'] > reject_thres and any(map(str.isalnum, word['text'])):
                        words.append(word['text'])
                if len(words) >= 2: # reject paragraph if less than 2 words
                    pars.append({
                        'pageNum': page['pageNum'],
                        'blockNum': block['blockNum'],
                        'parNum': par['parNum'],
                        'left': par['left'],
                        'top': par['top'],
                        'width': par['width'],
                        'height': par['height'],
                        'text': ' '.join(words)
                    })
    printMessage.end()
    return pars
