import scrapy

class LuontoporttiSpider(scrapy.Spider):
    name = "luontoportti"
    download_delay = 2.0

    def start_requests(self):
        urls = [
            'http://www.luontoportti.com/suomi/fi/sienet/?list=14',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        print("Parsed:",response.css("title::text").get())
        links = response.css("div#textlist a::attr(href)").getall()
        for link in links:
            yield response.follow(link, callback=self.parse_mushroom)

    def parse_mushroom(self, response):
        imagelinks = response.css("div#kuvat a::attr(href)").getall()
        name_fi = response.css("div#teksti h3::text").get()
        name_latin = response.css("div#teksti h4::text").get()
        info = response.css("div#teksti ul li::text").getall()
        yield { 'name_fi' : name_fi, 
                'name_latin' : name_latin,
                'info' : info,
                'image_urls' : imagelinks }
        pass