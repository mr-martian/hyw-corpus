#!/bin/bash

CORPUS=$1
ANALYSER=$2
LG=$(echo $CORPUS | sed 's:.*\/::' | sed -E 's:(.*\..*)\..*\.txt.*:\1:') # get corpus prefix

person=`whoami`
TMPPARADE=/tmp/$person.$LG.parade.txt

if [[ $1 =~ .*bz2 ]]; then
	CAT="bzcat"
else
	CAT="cat"
fi;

echo "Generating hitparade (might take a bit!)"

$CAT $CORPUS | apertium-destxt | lt-proc -w $ANALYSER | apertium-retxt | sed -E $'s/\\$[^^]*/\\$\\\n/g' > $TMPPARADE

echo "TOP UNKNOWN WORDS:"

cat $TMPPARADE | grep '\*' | sort | uniq -c | sort -rn | head -n20

TOTAL=`grep -v '^$' $TMPPARADE | wc -l`
KNOWN=`grep -v '^$' $TMPPARADE | grep -v '\*' | wc -l`
UNKNOWN=`grep -v '^$' $TMPPARADE | grep '\*' | wc -l`

PERCENTAGE=`echo $KNOWN/$TOTAL | calc -p | sed 's/[\s\t]//g'`

echo "coverage: $KNOWN / $TOTAL ($PERCENTAGE)"
echo "remaining unknown forms: $UNKNOWN"

DATE=`date`;
echo -e $LG $DATE"\t"$KNOWN"/"$TOTAL"\t"$PERCENTAGE >> history.log
tail -1 history.log