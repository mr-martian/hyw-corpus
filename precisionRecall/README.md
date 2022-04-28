The material was used for measuring precision and recall

 * [prec_rec.cg](prec_rec.cg.txt) and [prec_rec_cmd](prec_rec.cg.txt) have the program.

 * The files with the prefix `hyw-1500` are a set of 1500 tokens that was extracted. We then cleaned up these files to get the files with the prefix `hyw-1300`.

 * The reported stats from the paper are based on the `hyw-1300` files.

 * Use the following command:
	`python3 precisionRecall.py  hyw-1300.reference.txt  hyw-1300.annotated.txt`

 * How to generate the reference
   `cat hyw-1300.words.txt | hfst-proc -w ../../apertium-hyw/hyw.automorf.hfst | cg-conv -al > hyw-1300.reference.txt`
