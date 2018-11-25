# Tesseract OCR

## Introduction


Tesseract is a cross-platform OCR (Optical Character Recognition) engine which is compatible with major operating systems like Windows, Linux and Mac. It is a free software released under the Apache License 2.0. Tesseract was originally a proprietary software developed by Hewlett-Packard (HP) Labs between 1985 and 1994 and then became open-source in 2005. Since 2006, the Tesseract engine has been sponsored by Google and it has become one of the most popular and accurate OCR engines these days.

Tesseract supports Unicode characters and can recognise more than 100 languages. It can also be trained to recognise new languages by feeding external training data. The latest version 4.0 adds an LSTM-based engine which makes the recognition even more accurate. However, this latest version is not a stable version and is under active development.

## Evolution

### Version 1 & 2

Early versions of Tesseract could only accept TIFF images and did not have page-layout analysis. Therefore, they could only recognise images of simple one-column text. Also, these early versions could only support a few western languages like English, French and German.

### Version 3

Since Version 3, the engine has supported output text formatting and page-layout analysis which has introduced new capability of multi-columned text recognition compared to previous versions. In addition, a lot more languages are supported in this version, including ideographic languages like Chinese and Japanese and right-to-left languages like Arabic. Version 3 also added support for PNG images as input.

### Version 4

Version 4 has included a new neural network (LSTM) based engine, which significantly improves the recognition accuracy. It now supports 116 languages in total.

## Installation (Mac)

For Macintosh machines, Tesseract 3.x (the latest stable version) can be installed very easily via the third-party package manager Homebrew by running: `brew install tesseract`.

In order to install the most recent version 4.x we need to [build from source](https://github.com/tesseract-ocr/tesseract/wiki/Compiling#macoslink).

## Command Line Usage

The Tesseract engine itself is written in C++ and can only be executed from command line, which also means that there are no official GUIs associated with the engine. This section introduces basic usage of the command line program of Tesseract. More info about command line usage [here](https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage).

### Main Command

`tesseract imagename outputbase [-l lang] [--oem ocrenginemode] [--psm pagesegmode]
[configfiles...]`

### OCR Engine Mode (--oem)

There are 2 engines (Legacy and LSTM) and 4 engine modes available in Tesseract:

| Mode | Description |
|:----:|-------------|
| 0 | Legacy engine only (version 3 or lower) |
| 1 | Neural nets LSTM engine only (version 4) |
| 2 | Legacy + LSTM engines (version 4) |
| 3 | Default, based on what is available |

We can use legacy engine or LSTM engine only, or a combination of two.

### Page Segmentation Mode (–psm)

There are 13 segmentation modes in total. Four major modes are shown as follows:

| Mode | Description |
|:----:|-------------|
| 0 | Orientation and script detection (OSD) only |
| 1 | Automatic page segmentation with OSD |
| 2 | Automatic page segmentation, but no OSD, or OCR |
| 3 | Fully automatic page segmentation, but no OSD (Default) |

Orientation and script detection (OSD) automatically detects the principal orientation of the input document. With OSD, we can still process an input image with reasonable accuracy even if it has been rotated by some angle.

**Difference between mode 0 and 1**: Mode 0 only outputs OSD data like the rotation angle and associated confidence score, whilst mode 1 outputs the full recognition result along the principal angle computed by OSD.

## PyTesseract

PyTesseract is a python wrapper for the Tesseract command line program. The original Tesseract program must be installed before using the PyTesseract wrapper.

### Installation

`pip install pytesseract`

### Documentation

https://pypi.org/project/pytesseract/

### API

Full API documentation is accessible from the above link. The most useful API function is `pytesseract.image_to_data`, which returns a table containing box boundaries, confidence scores and other information for each recognised text box. The columns of the returned table are:

* **level**: the level number of the box. 5 levels in total
* **page_num**: page number. Page is the first level box.
* **block_num**: block number. Block is the second level box.
* **par_num**: paragraph number. Paragraph is the third level box.
* **line_num**: line number. Line is the fourth level box.
* **word_num**: word number. Word is the fifth level box.
* **left**: left margin of the box (in pixels)
* **top**: top margin of the box (in pixels)
* **width**: width of the box (in pixels)
* **height**: height of the box (in pixels)
* **conf**: confidence score for the box. Only valid for word-level boxes. For other 4 levels, this value is always -1.
* **text**: the recognised text for word-level boxes. Value is empty for other four levels.

## Confidence Score

Tesseract provides a confidence score for each recognised word. 

I picked a very long word (namely `PNEUMONOULTRAMICROSCOPICSILICOVOLCANOCONIOSIS`) to test the relationship between the confidence score and the correctness of recognition. By adding random noise to the image of the long word and testing the correctness of the recognised word, I have produced around 400 recognition results and they are logged in [`confidence.log`](./confidence.log)

The `confidence.log` has two columns. Each row is an outcome of the recognition. For each outcome, the first column is the associated confidence score and the second column is the correctness of the recognition (True/False). According to the result, we can summarise as follows:

- confidence above 80: actual accuracy around 90%
- confidence 60 - 80: actual accuracy around 70%
- confidence 40 - 60: actual accuracy around 45%
- confidence below 40: actual accuracy around 30%

In practice, a threshold of 75 for the confidence score is a relatively reasonable choice.