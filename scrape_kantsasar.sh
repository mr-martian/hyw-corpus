#!/bin/bash

cd crawlers

dt=`date '+%Y%m%d'`
scrapy crawl kantsassar -O "../Newspaper/hyw.kantsasar.$date.json"
