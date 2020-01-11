import scrapy
from scrapy.utils.url import urljoin_rfc

class AveyronSpider(scrapy.Spider):
    name = "aveyron"
    download_delay = 2.0

    def start_requests(self):
        urls = [
            'http://champignons.aveyron.free.fr/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response):
        print("Parsed:",response.css("title::text").get())
        for match in response.css("div#sidebar_bottom li:not(.group) a"):
            #text = match.css("a::text").get()
            link = match.attrib["href"]
            yield response.follow(link, callback=self.parse_mushroom)

    def parse_mushroom(self, response):
        imagelinks = response.css("img.photo_champi::attr(src)").getall()
        name_fr = response.css("div#main_info h1::text").get()
        name_latin = response.css("div#main_info h2::text").get()
        if ": " in name_latin: name_latin = name_latin.split(": ")[1]
        info = "".join(response.css("div.main_information::text").getall())
        yield { 'name_fr' : name_fr, 
                'name_latin' : name_latin,
                'info' : info,
                'image_urls' : [str(urljoin_rfc(response.url, relative), "ascii") for relative in imagelinks] }
        pass