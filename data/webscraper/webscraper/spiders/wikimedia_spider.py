import scrapy
from scrapy.utils.url import urljoin_rfc

class FirstNatureSpider(scrapy.Spider):
    name = "firstnature"
    download_delay = 1

    def start_requests(self):
        urls = [
            'https://www.first-nature.com/fungi/index1binom.php',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        print("Parsed:",response.css("title::text").get())
        for link in response.css("tr td em a::attr(href)").getall():
            yield response.follow(link, callback=self.parse_mushroom)

    def parse_mushroom(self, response):
        imagelinks = response.css("img[src^=images]:not([alt*=Spore]):not([alt*=Basidiospore]):not([alt*=Clamidia])::attr(src)").getall()
        name_latin = response.css("h1 i::text").get()
        if not name_latin:
            name_latin = response.css("h1 em::text").get()
        yield { 'name_latin' : name_latin,
                'image_urls' : [str(urljoin_rfc(response.url, relative), "ascii") for relative in imagelinks] }
        pass