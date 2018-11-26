# Alignment Algorithm

## Introduction

The handout-to-audio alignment algorithm is the core part of the system. The alignment algorithm takes as inputs the extracted chunks of handout text and segments of transcribed audio and then perform matching between handout chunks and audio segments.

The current algorithm used is based on the word-level `diff`.

## The diff algorithm

`diff` is a command-line program which compares two text files and find the differences between them. It tries to find the maximum common subsequence between two sequences, which in essence is a dynamic programming (DP) problem.

The normal `diff` operates at line-level, which takes lines as the basic units of comparison. The current alignment algorithm uses the word-level `diff`, where the basic unit of comparison is word.

## Algorithm

We first concatenate the recognised handout chunks in `source-code/output/paragraphs.json` and also concatenate transcript segments in `source-code/output/transcript.json` into two long strings. Then we eliminate all non-alphanumeric characters in these strings and extract individual words from them. 

Once we have the two word-sequences ready, we can then perform the word-level diff on these sequences. **We map a handout chunk to an audio segment if they share a matching sequence of at least 3 words**. The matching sequences can be seen from the output from the word-level diff.

## Evaluation

For each generated handout chunk we manually find the correct match within the audio segments and hence produce a 'ground truth' result. We then compare the alignment result from our algorithm with the 'ground-truth' result and calculate the accuracy for the alignment process.

## Performance

Alignment performance is tested informally on various data sources.

### Coursera online course for TCP/IP (4 slides)

Most of the time the lecturer just read the lecture slides verbatim, so the alignment accuracy is 90%, which is very high.

### Dr Rich Turner's course for Gaussian Process (1 slide)

The lecturer explained a lot on this slide and rephrased a lot when he referred to the slide content, so the accuracy is only 50%.