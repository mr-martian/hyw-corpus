#!/bin/bash

cd crawlers

dt=`date '+%Y%m%d'`
python3 -m scrapy crawl kantsassar -O "../Newspaper/hyw.kantsasar.$date.json"
