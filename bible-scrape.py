#!/usr/bin/env python3
import requests
from html.parser import HTMLParser
from html.entities import name2codepoint

writing = False
out = None

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global writing, out
        if tag == 'div':
            if dict(attrs).get('class') in ['usfm_s1', 'usfm_p']:
                writing = True
            else:
                writing = False
        elif tag == 'b' and writing:
            out.write('\n')
        elif tag == 'title':
            writing = True

    def handle_endtag(self, tag):
        global writing
        if tag == 'title' or tag == 'div':
            writing = False

    def handle_data(self, data):
        global writing, out
        if writing:
            if not out:
                out = open('Bible/' + data + '.txt', 'w')
            else:
                out.write(data.replace(' ', ' '))

with open('Bible_links.txt') as fin:
    for line in fin:
        parser = MyHTMLParser()
        r = requests.get(line.strip())
        parser.feed(r.text)
        out.close()
        out = None
