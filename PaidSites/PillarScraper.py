import scrapy
from scrapy.crawler import CrawlerProcess

class PillarSpider(scrapy.Spider):
    name = "Pillar"
    allowed_domains = ["pillarnonprofit.ca"]
    start_urls = ["https://pillarnonprofit.ca/membership/membership-directory"]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'PillarData2.csv',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    }

    def parse(self, response):
        Tags = response.xpath('//td[@class="views-field views-field-display-name active"]/text()[normalize-space()]').getall()
        for tag in Tags:
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
    process.crawl(PillarSpider)
    process.start()
