import modules.handoutProcess as hp
import modules.audioProcess as ap
from modules.alignment import align
import json

config = json.load(open('config.json'))

# handout processing
if not config['handoutProcess']['skip']:
    print('[HANDOUT PROCESS BEGIN]')
    images = hp.pdf_to_images(config['handoutProcess']['abspath'])
    obj = hp.images_to_obj(images)
    paragraphs = hp.obj_to_pars(obj, config['handoutProcess']['reject_thres'])
    json.dump(paragraphs, open('output/paragraphs.json', 'w'), indent=4)
    print('[HANDOUT PROCESS FINISHED]')
else:
    paragraphs = json.load(open('output/paragraphs.json'))
    print('[SKIPPED HANDOUT PROCESS]')

# audio processing
if not config['audioProcess']['skip']:
    print('[AUDIO PROCESS BEGIN]')
    transcript = ap.transcribe_gcs(config['audioProcess']['gcs_uri'])
    json.dump(transcript, open('output/transcript.json', 'w'), indent=4)
    print('[AUDIO PROCESS FINISHED]')
else:
    transcript = json.load(open('output/transcript.json'))
    print('[SKIPPED AUDIO PROCESS]')

# alignment
print('[ALIGNMENT BEGIN]')
align_result = align(paragraphs, transcript)
json.dump(align_result, open('output/alignment.json', 'w'), indent=4)
print('[ALIGNMENT FINISHED]')