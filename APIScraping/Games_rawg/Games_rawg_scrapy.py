import scrapy
import json
from scrapy.crawler import CrawlerProcess

class GamesSpider(scrapy.Spider):
    name = 'games'
    start_urls = ['https://rawg.io/api/games?page=1&page_size=40&filter=true&comments=true&key=c542e67aec3a4340908f9de9e86038af']
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'GamesData.csv',
        'concurrent_requests': 15
    }

    def parse(self, response):
        data = json.loads(response.body)
        results = data.get('results', [])

        for result in results:
            genre_names = [genre['name'] for genre in result.get('genres', [])]
            platform_names = [platform['platform']['name'] for platform in result.get('platforms', [])]
            store_names = [store['store']['name'] for store in result.get('stores', [])]
            esrb_rating = result.get('esrb_rating')
            yield{
                'ID' : result.get('id'),
                'Name': result.get('name'),
                #'Ratings': result.get('rating'),
                #'Ratings count' : result.get('ratings_count'),
                #'Released Date' : result.get('released'),
                'Genres' : genre_names,
                #'Platforms': platform_names,
                #'Stores' : store_names,
                #'ESRB Rating' : esrb_rating['name'] if esrb_rating else None,
                'Image_url' : result.get('background_image'),
            }

        next_page = data.get('next')
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    })
    process.crawl(GamesSpider)
    process.start()