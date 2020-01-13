#!/usr/bin/env bash
scrapy crawl luontoportti -o json/luontoportti.json
scrapy crawl aveyron -o json/aveyron.json
scrapy crawl firstnature -o json/firstnature.json
scrapy crawl expert -o json/expert.json
scrapy crawl wikimedia # output handled by pipeline