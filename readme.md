# CUED Part IIB Project - Talking Handouts

## Directory Tree

* [algorithms](./algorithms)
* [source-code](./source-code)
* [tools-doc](./tools-doc)

## Introduction

This is the main project folder for the CUED Part IIB fourth year project - **Talking Handouts**. 

This project is supervised by Prof. Phil Woodland and Dr. Chao Zhang.

## Project Description

Some Part 1 engineering lectures are currently being recorded and available for students to listen to later and can optionally have captions associated with them. The captions can allow a simple search mechanism. If these captions are to be generated automatically via speech recognition then it is very useful if the speech recogniser has access to the information in the handouts/slides and this can give significantly reduced error rates. The time alignment with the video is solved by the speech recogniser output.

The aim of this project is to investigate an alternative style of interface to the video/audio lecture information that is is based on the handouts/slides themselves, with the aim to provide direct links from the handouts/slides to the associated part of the lecture(s). This is termed "talking handouts", and the aim of this project is to investigate this idea.

Particular sub-problems to be addressed could include:
- Alignment of the generated audio to the handout/slides when the handout itself isn't a literal representation of what has been said. Note that individual handouts might cover several lectures
- Dealing with spoken forms of equations
- Dealing with handouts with significant "gaps" which are filled in with handwritten notes which include the 1A and 1B lectures currently being recorded
- Improving speech recognition output by adapting the language model of the speech recogniser based on the handout material and the acoustic model based on a significant amount of automatic transcripts from the same speaker.

The aim would be to process the pdf forms of handouts/slides and be able to "align" spoken information to the slides at the granularity of individual slides.

## Objectives

1. Investigate methods of extracting printed text from PDFs of handouts, including symbols & equations
2. Investigate extracting hand-written text etc. from PDFs of scanned handouts using OCR methods
3. Investigate possible ways lecturers refer to equations and figures
4. Investigate use of speech-recognition based alignment of handout text to audio
5. Investigate & evaluate creating links to audio from portions of handouts (at different levels)

## Links

- [Part IIB projects: second notice](http://teaching.eng.cam.ac.uk/content/part-iib-projects-second-notice)