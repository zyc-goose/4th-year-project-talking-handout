# Source Code

## Directory Tree

* [modules](./modules)
    * [alignment.py](./modules/alignment.py)
    * [audioProcess.py](./modules/audioProcess.py)
    * [handoutProcess.py](./modules/handoutProcess.py)
    * [printMessage.py](./modules/printMessage.py)
* [output](./output)
    * [alignment.json](./output/alignment.json)
    * [paragraphs.json](./output/paragraphs.json)
    * [transcript.json](./output/transcript.json)
* [config.json](./config.json)
* [main.py](./main.py)

## Documentation

### modules

Folder which contains core Python modules in the current system. These modules are:

* **alignment.py**: core algorithm for handout-audio alignment
* **audioProcess.py**: transcribe lecture audio using Google Cloud
* **handoutProcess.py**: extract information from handouts using Tesseract
* **printMessage.py**: auxiliary module to help print interactive messages

For more information, see [here](./modules).

### output

Folder which stores results produced by the system. Currently they are all in JSON format.

* **alignment.json**: the final handout-audio alignment result
* **paragraphs.json**: the extracted text from the handout input, organised in a list of paragraphs
* **transcript.json**: the produced transcript of the corresponding lecture audio

For more information, see [here](./output).

### config.json

The main configuration file which specifies the core parameters of the system, for example the absolute path for the handout input.

* **"handoutProcess"**
    * **"skip"**: [boolean] if true, skip the handout process stage
    * **"abspath"**: [string] the absolute path of the handout input
    * **"reject_thres"** [number] the confidence threshold below which a word should be discarded. Range from 0-100. Usually 70-80.
* **"audioProcess"**
    * **"skip"**: [boolean] if true, skip the audio process stage
    * **"gcs_uri"**: [string] the Google Cloud URI of the input audio file, which should be already uploaded to Google Cloud Storage. 

### main.py

The main Python script which performs all procedures involved in the current system, including handout processing, audio processing and handout-to-audio alignment. Type `python main.py` to run the script. The results will be stored in the `output` folder.