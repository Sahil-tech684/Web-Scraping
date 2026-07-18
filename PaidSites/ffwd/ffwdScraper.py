import scrapy
from scrapy.crawler import CrawlerProcess

class ffwdSpider(scrapy.Spider):
    name = 'ffwd'
    start_urls = ["https://www.ffwd.org/tech-nonprofits/"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'ffwdData.csv',
        #'LOG_LEVEL' : 'Error',
    }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    }


    def parse(self, response):
        links = response.css('li.row article.directory-content h2 a::attr(href)').getall()
        for link in links:
            url = str(link)
            yield scrapy.Request(url, callback=self.parse_page, headers=self.HEADERS)

        next_page = response.css('a.nextpostslink::attr(href)').get()
        if next_page:
            next_page_url = 'https://www.ffwd.org' + str(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse, headers=self.HEADERS)

    def parse_page(self, response):
        content = response.css('section.directory-details > div.row > div.col-sm-6 li')
        content2 = response.css('section.directory-details > div.row > div.col-xs-12.col-sm-6 li')
        yield{
            'Name' : response.css('div.col-sm-8 > h1::text').get().strip(),
            'Descp1' : response.css('div.entry-excerpt > p::text').get().strip() if response.css('div.entry-excerpt > p::text') else None,
            'Descp2' : response.css('section.directory-details > div.row > div.col-sm-12 > p::text').get().strip() if response.css('section.directory-details > div.row > div.col-sm-12 > p::text') else None,
            'FoundedIn' : response.css('div.col-sm-8 > p.founded::text').getall()[1].strip(),
            'FoundersName' :  response.css('div.col-sm-8 > p.founded > a::text').getall(),
            'FoundersLinkedIn' : response.css('div.col-sm-8 > p.founded > a::attr(href)').getall(),
            'URL' : response.css('p.connect-links > a::attr(href)').get(),
            'Program Area' : content.css('span.block::text').getall()[0],
            'Location of Impact' : content.css('span.block::text').getall()[1],
            'Headquarters Location' : content.css('span.block::text').getall()[2],
            'Product platforms' : content2.css('li span.block::text').getall()[0] if content2.css('li span.block::text') else None,
            'Budget' : content2.css('li::text').get(),
        }

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(ffwdSpider)
    process.start()