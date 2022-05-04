#!/bin/bash

cd crawlers

dt=`date '+%Y%m%d'`
python3 -m scrapy crawl kantsasar -O "../Newspaper/hyw.kantsasar.$dt.json"
