import scrapy
from scrapy.crawler import CrawlerProcess

class norrskenSpider(scrapy.Spider):
    name = 'norrsken'
    start_urls = ["https://www.norrsken.org/impact100#"]
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'norrskenData.csv',
        #'LOG_LEVEL' : 'Error',
    }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    }

    def parse(self, response):
        contents = response.css('section.section-2603.section2.list div.w-dyn-list div[role="listitem"].w-dyn-item')
        for content in contents:
            yield{
                'Name' : content.css('div.w-layout-grid.grid-298 > h1::text').get() if content.css('div.w-layout-grid.grid-298 > h1::text') else content.css('div.w-layout-grid.grid-298 > h2::text').get(),
                'Sector' : content.css('div.w-layout-grid.grid-298 > div[fs-cmsfilter-field="Sector"]::text').get() if content.css('div.w-layout-grid.grid-298 > div[fs-cmsfilter-field="Sector"]::text') else content.css('div.w-layout-grid.grid-298 > div[id="w-node-b21c7eb9-2ab5-c5be-6269-14dbd1304d0b-27453b17"]::text').get(),
                'Country' : content.css('div.w-layout-grid.grid-298 > div[fs-cmsfilter-field="Geography"]::text').get(),
                'Year' : content.css('div.w-layout-grid.grid-298 > div[fs-cmsfilter-field="year"]::text').get(),
                'Descp' : content.css('div.w-layout-grid.grid-299 > p::text').get(),
                'URL' : content.css('div.w-layout-grid.grid-299 > a::attr(href)').get(),
            }


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(norrskenSpider)
    process.start()