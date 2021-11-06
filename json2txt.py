#!/usr/bin/env python3

import json

with open('kantsasar.json') as fin:
    blob = json.load(fin)
    with open('hyw.kantsasar.20211104.txt', 'w') as fout:
        count = 0
        for art in blob:
            if "ա" in art['body'] and "ا" not in art['body']:
                count += 1
                fout.write(art['title'] + '\n')
                fout.write(art['body'] + '\n\n')
        print(count, 'total articles extracted')
