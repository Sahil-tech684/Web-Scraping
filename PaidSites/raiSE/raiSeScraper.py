import scrapy
from scrapy.crawler import CrawlerProcess

class raiSeSpider(scrapy.Spider):
    name = 'raiSe'
    start_urls = ["https://www.raise.sg/directory/directories/default.html?pbs=null&start=0"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'raiSeData.csv',
        #'LOG_LEVEL' : 'Error',
    }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    }


    def parse(self, response):
        links = response.css('div.col-md-4 div.intro-image a::attr(href)').getall()
        for link in links:
            url = 'https://www.raise.sg' + str(link)
            yield scrapy.Request(url, callback=self.parse_page, headers=self.HEADERS)

        start_param = int(response.url.split('=')[-1])
        next_start = start_param + 15
        next_page_url = f'https://www.raise.sg/directory/directories/default.html?pbs=null&start={next_start}'
        yield scrapy.Request(next_page_url, callback=self.parse, headers=self.HEADERS)

    def parse_page(self, response):
        content = response.css('div.service > div.intro')
        yield{
            'Name' : response.css('div.content > h3.title::text').get(),
            'Name of Business' : str(response.css('div.main-infor div.intro-text p::text').getall()[1]).strip() if response.css('div.main-infor div.intro-text p::text') else None,
            'Area of Impact' : str(response.css('div.main-infor div.intro-text p::text').getall()[3]).strip() if response.css('div.main-infor div.intro-text p::text') else None,
            'URL' : response.css('div.content > a.website::attr(href)').get(),
            'Descp' : content[0].css('p::text').getall(),
            'Product & Services' : content[1].css('p::text').getall(),
            'Contact' : response.css('div.content > div.note a::text').get()
        }

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(raiSeSpider)
    process.start()