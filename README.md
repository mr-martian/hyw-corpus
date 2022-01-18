# hyw-corpus

## Overview
This repo contains the corpora that we used to evaluate the Apertium morphological analyzer for [Western Armenian](https://github.com/apertium/apertium-hyw/). We created corpora through a mix of manual and automated scraping. The different corpora are stored in the different subfolders. Each folder has a README file that explains the individual corpora and how we used them.

The corpora and the folders are the following:

* [Bibles](Bibles/) for Western and Eastern Armenian
* A [Newspaper](Newspaper/) corpus for Western Armenian
* [UD](UD/) Treebanks for Western and Eastern Armenian
* [Wikipedia](Wikipedia/) for Western and Eastern Armenian

To measure precision and recall, we used the items and code in the [precision_recall_material](precision_recall_material/) folder. 

## Helpful commands

To evaluate the analyzer over some corpus, do the following:

1. Clone this repo and the [apertium-hyw](https://github.com/apertium/apertium-hyw/) repo.
2. To get the analyzer, run `make hyw.automorf.bin` or `make`.
3. To run the analyzer on some corpus (`CORPUS`), run the following command:
`sh coverage-ltproc.sh CORPUS ../apertium-hyw/hyw.automorf.bin`
4. Open the temp folder by running the following command:
	 `open /tmp`
5. Find the filename of the parade file and copy the file name. 
The file name can look something like `CORPUS.parade.txt`
6. To get a list of tokens and their analysis, run the following command:
`cat /tmp/CORPUS.parade.txt | lt-proc ../apertium-hyw/hyw.automorf.bin | apertium-cleanstream -n > toks.txt`
7. To get a list of unknown tokens, run the following command:
`cat /tmp/CORPUS.parade.txt | grep '\*' | sort | uniq -c | sort -rn > unks.txt`







