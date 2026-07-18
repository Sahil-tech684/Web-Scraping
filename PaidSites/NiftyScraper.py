import scrapy
from scrapy.crawler import CrawlerProcess
import json

class NiftySpider(scrapy.Spider):
    name = 'Nifty'
    allowed_domains = ["api.niftygateway.com"]
    start_urls = ["https://api.niftygateway.com/stats/rankings/?page=1&page_size=50&sort=-seven_day_total_volume"]

    custom_settings = {
        'FEEDS': {
            'NiftyData.csv': {
                'format': 'csv',
            },
        },
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
        'Origin': 'https://www.niftygateway.com',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.niftygateway.com/',
        'Connection': 'keep-alive',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.HEADERS, callback=self.parse)

    def parse(self, response):
        data = json.loads(response.body)
        results = data.get('results', [])
        for result in results:
            collections = result.get('collection', [])
            if isinstance(collections, list):
                for collection in collections:
                    title = collection.get('niftyTitle', '')
                    yield {
                        'title': title,
                        'total_volume': float(result.get('sevenDayTotalVolume', 0)) / 100,
                        'no._of_sales': result.get('sevenDayNumTotalSales', 0),
                        'sales_floor': float(result.get('floorPrice', 0)) / 100,
                        'avg_price': float(result.get('avgSalePrice', 0)) / 100,
                        'items': result.get('totalSupply', 0),
                        'owners': result.get('numOwners', 0),
                    }
            elif isinstance(collections, dict):
                    title = collections.get('niftyTitle', '')
                    yield {
                        'title': title,
                        'total_volume': float(result.get('sevenDayTotalVolume', 0)) / 100,
                        'no._of_sales': result.get('sevenDayNumTotalSales', 0),
                        'sales_floor': float(result.get('floorPrice', 0)) / 100,
                        'avg_price': float(result.get('avgSalePrice', 0)) / 100,
                        'items': result.get('totalSupply', 0),
                        'owners': result.get('numOwners', 0),
                    }


        next_page = data.get('next')
        if next_page:
            yield scrapy.Request(url=next_page, headers=self.HEADERS, callback=self.parse)

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(NiftySpider)
    process.start()
