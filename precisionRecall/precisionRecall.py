#!/usr/bin/env python3

import argparse
from subprocess import Popen, PIPE
import re
import sys

reToken = re.compile("\^.*?\$")
reForm = re.compile("\^(.*?)\/")
reAnalyses = re.compile("\/([^\*].*?)\$")

def convertToApertium(fn):
	p1 = Popen(["cat", fn], stdout=PIPE)
	p2 = Popen(["cg-conv", "-Al"], stdin=p1.stdout, stdout=PIPE)
	p1.stdout.close()
	APdata = p2.communicate()[0].decode()
	return APdata

def getCohorts(refTokens, annTokens):
	refCohorts = {}
	annCohorts = {}
	for tok in refTokens:
		if reAnalyses.search(tok):
			refCohorts[reForm.match(tok).groups()[0]] = reAnalyses.search(tok).groups()[0].split('/')
		else:
			refCohorts[reForm.match(tok).groups()[0]] = None
	for tok in annTokens:
		if reAnalyses.search(tok):
			annCohorts[reForm.match(tok).groups()[0]] = reAnalyses.search(tok).groups()[0].split('/')
		else:
			annCohorts[reForm.match(tok).groups()[0]] = None
	extraCohorts = []
	for lem in refCohorts:
		if lem not in annCohorts:
			extraCohorts.append(lem)
	for lem in annCohorts:
		if lem not in refCohorts:
			extraCohorts.append(lem)

	return refCohorts, annCohorts, extraCohorts


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='calculate precision and recall on a reference corpus relative to an annotated corpus')
	parser.add_argument('-a', '--apertium', action='store_true', default=False,
		help='Assume Apertium stream format')
	parser.add_argument('-c', '--cg', action='store_true', default=True,
		help='Assume CG format (default)')
	parser.add_argument('-v', '--verbose', action='store_true', default=False,
		help='Show counts for each form')
	parser.add_argument('-e', '--errors', action='store_true', default=False,
		help='Show errors found')
	parser.add_argument('-i', '--ignore', action='store_true', default=False,
		help='ignore forms in reference that aren\'t annotated (as opposed to erroring out)')
	parser.add_argument('-p', '--precision', action='store_true', default=False,
		help='show precision results only, rounded to 2 decimal places')
	parser.add_argument('-r', '--recall', action='store_true', default=False,
		help='show recall results only, rounded to 2 decimal places')
	parser.add_argument('reference_corpus', help='reference corpus (output of transducer)')
	parser.add_argument('annotated_corpus', help="hand-annotated corpus (gold standard)")

	args = parser.parse_args()

	# open files
	if args.cg and not args.apertium:
		refSents = convertToApertium(args.reference_corpus)
		annSents = convertToApertium(args.annotated_corpus)
	elif args.apertium:
		with open(args.reference_corpus, 'r') as f_ref:
			refSents = f_ref.read()
		with open(args.annotated_corpus, 'r') as f_ann:
			annSents = f_ann.read()

	# get all tokens
	refTokens = reToken.findall(refSents)
	annTokens = reToken.findall(annSents)

	refCohorts, annCohorts, extraCohorts = getCohorts(refTokens, annTokens)

	# sanity checks
	if (len(refTokens) != len(annTokens)):
		#print("ref: "+",".join(refCohorts))
		#print("ann: "+",".join(annCohorts))
		#print(annCohorts)

		if not args.ignore:
			print("ERROR: different number of annotated ({}) and reference ({}) cohorts; check these: {}".format(len(annTokens), len(refTokens), ", ".join(extraCohorts)))
			sys.exit()
		else:
			refTokens = [item for item in refTokens if item not in annTokens]
	elif (len(refTokens)==0 and len(annTokens)==0 and args.apertium):
		print("ERROR: can't find tokens; probably not apertium stream format; try without -a")
		sys.exit()
	elif (len(refTokens)==0):
		print("ERROR: no tokens found!")
		sys.exit()
	#else:
	#	print("ERROR: unknown")
	#	sys.exit()


	# {total, false} {negatives, positives}
	tp, fp, tn, fn = 0, 0, 0, 0

	if not args.ignore:
		# the old way: loop tokens of each in parallel
		for (refTok, annTok) in zip(refTokens, annTokens):
			# get lemmas
			refLem = reForm.match(refTok).groups()[0]
			annLem = reForm.match(annTok).groups()[0]

			# one last sanity check
			if refLem != annLem:
				print("ERROR: reference lemma '{}' doesn't match annotated lemma '{}'".format(refLem, annLem))
				sys.exit()
			else:
				# get analyses, can be empty if starts with '*'
				refAnalysesMatches = reAnalyses.search(refTok)
				refAnalyses = (refAnalysesMatches.groups()[0].split('/') if refAnalysesMatches else [])
				annAnalysesMatches = reAnalyses.search(annTok)
				annAnalyses = (annAnalysesMatches.groups()[0].split('/') if annAnalysesMatches else [])

				# measure numbers for this token
				thisTp, thisFp, thisTn, thisFn = 0, 0, 0, 0
				for refAnalysis in refAnalyses:
					if refAnalysis in annAnalyses:
						thisTp += 1
					else:
						thisFp += 1
				for annAnalysis in annAnalyses:
					if annAnalysis not in refAnalyses:
						thisFn += 1

				tp += thisTp
				fp += thisFp
				tn += thisTn
				fn += thisFn

				# show numbers for this token if verbose
				if args.verbose:
					print("{}: {} tp, {} fp, {} tn, {} fn".format(refLem, thisTp, thisFp, thisTn, thisFn))
				elif args.errors and (thisFp!=0 or thisTn!=0 or thisFn!=0):
					print("{}: {} tp, {} fp, {} tn, {} fn".format(refLem, thisTp, thisFp, thisTn, thisFn))
	else:
		# the better way:
		for form in annCohorts:
			if form not in refCohorts:
				print("ERROR: annotated lemma '{}' not in reference".format(form))
				sys.exit()
			else:
				# get analyses, potentially None
				refAnalyses = refCohorts[form]
				annAnalyses = annCohorts[form]

				# measure numbers for this token
				thisTp, thisFp, thisTn, thisFn = 0, 0, 0, 0
				if refAnalyses != None:
					for refAnalysis in refAnalyses:
						if refAnalysis in annAnalyses:
							thisTp += 1
						else:
							thisFp += 1

				for annAnalysis in annAnalyses:
					if refAnalyses == None:
						thisFn += 1
					else:
						if annAnalysis not in refAnalyses:
							thisFn += 1

				if args.verbose:
					print(refAnalyses, annAnalyses)
				#elif args.errors and (thisFp!=0 or thisTn!=0 or thisFn!=0):
				#	print(refAnalyses, annAnalyses)

				tp += thisTp
				fp += thisFp
				tn += thisTn
				fn += thisFn

				# show numbers for this token if verbose
				if args.verbose:
					print("{}: {} tp, {} fp, {} tn, {} fn".format(form, thisTp, thisFp, thisTn, thisFn))
				elif args.errors and (thisFp!=0 or thisTn!=0 or thisFn!=0):
					print("{}: {} tp, {} fp, {} tn, {} fn — ".format(form, thisTp, thisFp, thisTn, thisFn), refAnalyses, annAnalyses)


	#print("Totals: {} tp, {} fp, {} tn, {} fn".format(tp, fp, tn, fn))
	# calculate results
	precision = 100 * tp / (tp + fp)
	recall = 100 * tp / (tp + fn)
	formCount = len(annCohorts)

	# print results
	if args.verbose: print()
	if not args.precision and not args.recall:
		print("Totals: {} forms, {} tp, {} fp, {} tn, {} fn".format(formCount, tp, fp, tn, fn))
		print("Precision: {:.5f}%\nRecall: {:.5f}%".format(precision, recall))
	elif args.precision:
		print("{:.2f}".format(precision))
	elif args.recall:
		print("{:.2f}".format(recall))