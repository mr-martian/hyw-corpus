cat hyw.kantsasar.20211104.txt | apertium -d ../apertium-hyw hyw-morph | apertium-cleanstream -n | sort -u | sort -R | head -n1500 | cg-conv -al > hyw-1500.reference.txt
