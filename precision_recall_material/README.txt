The material was used for measuring precision and recall

 * prec_rec.cg and prec_rec_cmd have the program

 * hyw-1500 is a set of 1500 tokens that was extracted. We then cleaned up this file to get hyw-1300

 * The reported stats from the paper are based on the hyw-1300 files

 * Use the following command:
	python3 precisionRecall.py  hyw-1300.reference.txt  hyw-1300.annotated.txt 