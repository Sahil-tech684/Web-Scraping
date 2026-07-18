import scrapy
import json
from scrapy.crawler import CrawlerProcess

class AdidasSpider(scrapy.Spider):
    name = "Adidas"
    allowed_domains = ["www.adidas.jp"]
    start_urls = ["https://www.adidas.jp/%E3%83%A1%E3%83%B3%E3%82%BA-%E3%82%B7%E3%83%A5%E3%83%BC%E3%82%BA%E3%83%BB%E9%9D%B4"]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'www_adidad_com_au.csv',
    }

    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Brave";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    def parse(self, response):
        Product_links = response.xpath('').getall()
        for link in Product_links:
            tag = tag.strip()
            links = response.css('td.views-field.views-field-display-name.active strong a::attr(href)').getall()
            for link in links:
                url = 'https://pillarnonprofit.ca' + str(link)
                yield scrapy.Request(url, callback=self.parse_page, headers=self.HEADERS, meta={'Tag': tag})

        next_page = response.css('li.pager-next a::attr(href)').get()
        if next_page:
            next_page_url = 'https://pillarnonprofit.ca' + next_page
            yield scrapy.Request(next_page_url, callback=self.parse, headers=self.HEADERS)

    def parse_page(self, response):
        yield{
            'Name' : response.css('div.views-field.views-field-display-name h2.field-content::text').get() if response.css('div.views-field.views-field-display-name h2.field-content::text') else None ,
            'Decp' : response.css('div.views-field.views-field-description-note-93 span p::text').getall() if response.css('div.views-field.views-field-description-note-93 span p::text') else None,
            'Mail' : response.css('div.views-field.views-field-php-5 a::attr(href)').get() if response.css('div.views-field.views-field-php-5 a::attr(href)') else None,
            'Link' : response.css('div.views-field.views-field-url span a::attr(href)').get() if response.css('div.views-field.views-field-url span a::attr(href)') else None,
            'Tags' : response.meta['Tag'],
            'Address' : response.css('div.views-field.views-field-php-3 span.field-content div.views-field span.field-content::text').getall() if response.css('div.views-field.views-field-php-3 span.field-content div.views-field span.field-content::text') else None,

        }

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    })
    process.crawl(AdidasSpider)
    process.start()