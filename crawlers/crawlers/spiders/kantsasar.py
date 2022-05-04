#!/usr/bin/env python3

import scrapy

class kantsasar_spider(scrapy.Spider):
    name = 'kantsasar'
    start_urls = ['http://www.kantsasar.com/news/']

    def parse(self, response):
        for block in response.css('div.mg-blog-post-box'):
            author = 'unknown'
            for s_ in block.css('article div[style="text-align: right;"] strong::text').getall():
                s = s_.strip()
                if not s:
                    continue
                author = s # give the last one on the page
            ls = []
            for s_ in block.css('article *::text').getall():
                s = s_.strip()
                if s == 'Post navigation':
                    break
                elif s:
                    ls.append(s)
            yield {
                'title': (block.css('h1 a::text').get() or '').strip(),
                'author': author,
                'date': (block.css('span.mg-blog-date::text').get() or '').strip(),
                'body': '\n'.join(ls)
            }
        links = ['h5.title a', 'div.nav-links a', 'article.bottom a']
        for l in links:
            yield from response.follow_all(css=l, callback=self.parse)
