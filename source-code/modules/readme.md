# modules

- [modules](#modules)
    - [alignment.py](#alignmentpy)
    - [audioProcess.py](#audioProcesspy)
    - [handoutProcess.py](#handoutProcesspy)
    - [printMessage.py](#printMessagepy)

---

## alignment.py

### Dependencies

* **difflib** - Python library which provides `diff` utilities

### Methods

---

#### align(pars, trans) -> align_result

##### description

Perform handout-audio alignment using word-level `diff`.

##### arguments

* **pars**: list of extracted paragraphs from handout, which has the same format as `output/paragraphs.json`
* **trans**: transcript of the lecture audio which has the same format as `output/transcript.json`

##### returns

* **align_result**: the final alignment result, which has the same format as `output/alignment.json`

---

## audioProcess.py

### Dependencies

* **google.cloud.speech** - Google Cloud Speech-to-Text API

### Methods

---

#### transcribe_gcs(gcs_uri) -> transcript

##### description

Asynchronously transcribes the audio file specified by the gcs_uri.

##### arguments

* **gcs_uri** - URI with format `gs://<bucket>/<path_to_audio>`

##### returns

* **transcript**: transcript of the specified audio, with the same format as `output/transcript.json`

---

## handoutProcess.py

### Dependencies

* **pytesseract**: Python wrapper for Tesseract OCR
* **pdf2image**: convert PDF file to PIL images
* **PIL.Image**: image processing toolkit

### Methods

---

#### pdf_to_images(abspath) -> images

##### description

Convert a single PDF file to a list of PIL images.

##### arguments

* **abspath**: absolute path of the input PDF file

##### returns

* **images**: list of converted PIL images

---

#### images_to_obj(images) -> obj

##### description

Process the PIL images using the OCR engine and store results in a Python dictionary.

##### arguments

* **images**: PIL images converted from PDF file

##### returns

* **obj**: a Python dict which stores all processing results from OCR engine

---

#### obj_to_pars(obj, reject_thres=75) -> pars

##### description

Convert OCR results (obj) to a list of paragraphs.

##### arguments

* **obj**: Python dict which stores all processing results from OCR
* **reject_thres**: rejection threshold for words based on confidence scores (default 75)

##### returns

* **pars**: a list of paragraph objects

---

## printMessage.py

### Dependencies

* **sys**: System module for Python

### Methods

---

#### begin(message) -> None

##### description

Print message to show that a process has been initiated.

##### arguments

* **message**: the message to be printed

##### returns
None

---

#### end() -> None

##### description

Print 'Done' to show that a process has been finished.

##### arguments

None

##### returns

None

---