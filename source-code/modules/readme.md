# modules

## alignment.py

### Dependencies

* difflib - Python library which provides `diff` utilities
* re - regular expression
* printMessage.py

Methods

#### align(pars, trans)

##### arguments

* pars: list of extracted paragraphs from handout, which has the same format as `output/paragraphs.json`
* trans: transcript of the lecture audio which has the same format as `output/transcript.json`

##### returns

* align_result: the final alignment result, which has the same format as `output/alignment.json`