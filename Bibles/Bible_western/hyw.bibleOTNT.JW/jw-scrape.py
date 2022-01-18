#!/usr/bin/env python3
import requests
from html.parser import HTMLParser
from html.entities import name2codepoint
import sys

out = None

writing = False

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global out, writing
        if tag == 'div':
            if dict(attrs).get('class') == 'scalableui':
                writing = True
            else:
                writing = False
        elif writing and tag in ['span', 'header', 'h1']:
            out.write('\n')
    def handle_data(self, data):
        global out, writing
        if writing:
            out.write(data.replace(' ', ' '))

ch_count = [50, 40, 27, 36, 34,
            24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10,
            42, 150, 31, 12, 8,
            66, 52, 5, 48, 12,
            14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4,
            28, 16, 24, 21,
            28,
            16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1,
            13, 5, 5, 3, 5, 1, 1, 1,
            22]

failed = []

start = 1
if len(sys.argv) > 1:
    start = int(sys.argv[1])

for book, cc in enumerate(ch_count, start=1):
    if book < start:
        continue
    out = open(f'JW/{book}.txt', 'w')
    for chapter in range(1, cc+1):
        print(book, chapter)
        r = requests.get(f'https://wol.jw.org/hyw/wol/b/r487/lp-r/sbi1/{book}/{chapter}')
        if r.status_code == 200:
            parser = MyHTMLParser()
            parser.feed(r.text)
        else:
            print('  status code:', r.status_code)
            failed.append(book)
            break
    out.close()
print(failed)
