import scrapy
from scrapy.crawler import CrawlerProcess

class FISpider(scrapy.Spider):
    name = "FI"
    allowed_domains = ["fi.co"]
    start_urls = ["https://fi.co/50-EMEA"]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'FI_EMEA_Data.csv',
    }

    def parse(self, response):
        blocks = response.css('div.flex.md\\:-mx-3.lg\\:-mx-4.justify-center.-my-2.md\\:-my-3.lg\\:-my-4.flex-wrap')
        for block in blocks:
            yield {
                'Name': block.css('div.w-full > a.appearance-none > div.p-7 > div.flex > h3.font-bold::text').get(),
                'Founders': block.css('div.w-full > a.appearance-none > div.flex > div.px-7 > p.text-base::text').get(),
                'Founders LinkedIn': block.css('div.p-4.py-7 > div.flex > div.shrink-0 a::attr(href)').get(),
                'Address': block.css('div.w-full > a.appearance-none > div.p-7 span::text').get(),
                'Link': block.css('div.lg\\:col-span-10 a::attr(href)').get(),
                'Decsp': block.css('div.w-full > a.appearance-none > div.p-7 p::text').get(),
            }

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    })
    process.crawl(FISpider)
    process.start()
