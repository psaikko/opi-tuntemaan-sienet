# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class WikimediaPipeline(object):

    def open_spider(self, spider):
        if spider.name == "wikimedia":
            self.items = dict()

    def close_spider(self, spider):
        if spider.name == "wikimedia":
            with open('json/wikimedia.json', 'w') as f:
                print("------------DEBUG------------")
                for k in self.items:
                    print(k, self.items[k])
                json.dump(list(self.items.values()), f)

    def process_item(self, item, spider):
        if spider.name == "wikimedia":
            if item.get('name_latin') and item.get('images'):
                name = item.get('name_latin')
                if name in self.items:
                    self.items[name]['images'] += item.get('images')
                    self.items[name]['image_urls'] += item.get('image_urls')
                else:
                    self.items[name] = dict(item)
            return item