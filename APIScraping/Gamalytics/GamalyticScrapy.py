import scrapy
import json
from scrapy.crawler import CrawlerProcess

class GamalyticsSpider(scrapy.Spider):
    name = "abc"
    start_urls = ["https://api.gamalytic.com/steam-games/list?fields=name,releaseDate,copiesSold,price,revenue,avgPlaytime,reviewScore,publisherClass,publishers,developers,id,steamId&page=0&limit=50"]
    custom_settings = {
        'FEED_FROMAT' : 'json',
        'FEED_URI' : 'Gamalytics.json',
    }
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        data = json.loads(response.text)
        results = data.get('result', [])
        IDs = []
        for result in results:
            ID = result.get('id')
            IDs.append(ID)
        for id in IDs:
            url = "https://api.gamalytic.com/game/" + str(id)
            yield scrapy.Request(url=url, callback=self.parse_page)
        
        next_page = data.get('next')
        if next_page and next_page.get('page'):
            next_page_url = f"https://api.gamalytic.com/steam-games/list?fields=name,releaseDate,copiesSold,price,revenue,avgPlaytime,reviewScore,publisherClass,publishers,developers,id,steamId&page={next_page.get('page')}&limit=50"
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_page(self, response):
        data = json.loads(response.text)
        yield{
            'Name' : data.get('name'),
            'Steam ID' : data.get('steamId'),
            'Reviews' : data.get('reviews'),
            'reviewScore' : data.get('reviewScore'),
            'price' : data.get('price'),
            'avgPlaytime' : data.get('avgPlaytime'),
            'copiesSold' : data.get('copiesSold'),
            'revenue' : data.get('revenue'),
            'developers' : data.get('developers'),
            'publishers' : data.get('publishers'),
            'genres' : data.get('genres'),
            'tags' : data.get('tags'),
            'languages' : data.get('languages'),
            'features' : data.get('features'),
            'Windows' : data.get('win'),
            'Mac' : data.get('mac'),
            'Linux' : data.get('linux'),
            'Description' : data.get('description'),
            'playtimeData' : data.get('playtimeData'),
            'followers' : data.get('followers'),
            'Rank' : data.get('rank'),
            'owners' : data.get('owners'),
            'players' : data.get('players'),

        }


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(GamalyticsSpider)
    process.start()