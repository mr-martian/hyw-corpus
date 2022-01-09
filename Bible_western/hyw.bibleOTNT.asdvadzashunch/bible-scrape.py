#!/usr/bin/env python3
import requests
from html.parser import HTMLParser
from html.entities import name2codepoint

writing = False
out = None
weird = False

out_all = open('Bible.txt', 'w')

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global writing, out, out_all, weird
        if tag == 'div':
            if dict(attrs).get('class') in ['usfm_s1', 'usfm_p', 'MsoNormal', 'usfm_q', 'usfm_sp']:
                writing = True
            else:
                writing = False
        elif tag == 'b' and writing:
            out.write('\n')
            out_all.write('\n')
        elif tag == 'title':
            writing = True

    def handle_endtag(self, tag):
        global writing, out, out_all
        if tag == 'div' and writing:
            out.write('\n')
            out_all.write('\n')
        if tag == 'title' or tag == 'div':
            writing = False

    def handle_data(self, data):
        global writing, out, out_all
        if writing:
            if not out:
                t = data.strip()
                out = open('Bible/' + t + '.txt', 'w')
                out_all.write('\n' + t + '\n\n')
            else:
                s = data.replace(' ', ' ')
                out.write(s)
                out_all.write(s)

class WeirdHTMLParser(MyHTMLParser):
    def handle_starttag(self, tag, attrs):
        global writing, out, out_all, weird
        if tag == 'title':
            writing = True
        elif tag == 'span' and weird:
            writing = True
        elif tag == 'div' and dict(attrs).get('class') == 'section js-section':
            weird = True
        elif tag == 'br':
            out.write('\n')
            out_all.write('\n')
    def handle_endtag(self, tag):
        global writing, out, out_all
        if tag == 'span' and writing:
            out.write(' ')
            out_all.write(' ')
        if tag == 'span' or tag == 'title':
            writing = False

with open('Bible_links.txt') as fin:
    for line in fin:
        ls = line.split()
        if len(ls) == 1:
            parser = MyHTMLParser()
            r = requests.get(line.strip())
            parser.feed(r.text)
        else:
            parser = WeirdHTMLParser()
            r = requests.get(ls[0])
            parser.feed(r.text)
        out.close()
        out = None
        weird = False

out_all.close()
