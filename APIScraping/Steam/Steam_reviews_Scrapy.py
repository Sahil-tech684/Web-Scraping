import scrapy
from scrapy.crawler import CrawlerProcess

class SteamSpider(scrapy.Spider):
    name = "Steam"
    allowed_domain=['steamcommunity.com']

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'Steam_reviews.json',
    }
    HEADERS = {
    #'Cookie': 'sessionid=0caefcc3cb363801182bd8e1; recentlyVisitedAppHubs=271590; timezoneOffset=19800,0; cookieSettings=%7B%22version%22%3A1%2C%22preference_state%22%3A2%2C%22content_customization%22%3Anull%2C%22valve_analytics%22%3Anull%2C%22third_party_analytics%22%3Anull%2C%22third_party_content%22%3Anull%2C%22utm_enabled%22%3Atrue%7D; steamCountry=NL%7C5f140f69051513e7a953cce0a9f79ac5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Avast/118.0.0.0',
    }


    def start_requests(self):
        url = 'https://steamcommunity.com/app/271590/homecontent/?userreviewsoffset=0&p=1&workshopitemspage=1&readytouseitemspage=1&mtxitemspage=1&itemspage=1&screenshotspage=1&videospage=1&artpage=1&allguidepage=1&webguidepage=1&integratedguidepage=1&discussionspage=1&numperpage=10&browsefilter=toprated&browsefilter=toprated&l=english&appHubSubSection=10&filterLanguage=default&searchText=&maxInappropriateScore=50&forceanon=1'
        yield scrapy.Request(url=url, headers=self.HEADERS, callback=self.parse_page, meta={'index': 0, 'cookie': 'app_impressions='})

    def parse_page(self, response):
        contents = response.css('div.apphub_UserReviewCardContent')
        reviews = response.xpath("//*[@class='apphub_Card modalContentLink interactable']")

        for content,review in zip(contents,reviews):
               yield{
                    'Date': content.css('div.date_posted::text').getall(),
                    'user_name': review.xpath(".//*[contains(@class, 'apphub_CardContentAuthorName')]/a/text()").get(),
                    'user_profile_url': review.xpath(".//*[contains(@class, 'apphub_CardContentAuthorName')]/a/@href").get(),
                    'Title': content.css('div.title::text').get(),
                    'Reaction': content.css('div.found_helpful::text').getall()[:2],
                    'Review': content.css('div.apphub_CardTextContent::text').getall()[1:]
                }

        params = {}
        for input_field in response.css('form[method="GET"] input[type="hidden"]'):
            param_name = input_field.attrib['name']
            param_value = input_field.attrib['value']
            params[param_name] = param_value

        i = response.meta['index'] + 1
        cookie = f"{response.meta['cookie']}|271590@2_9_100010_" if i else f"{response.meta['cookie']}730@2_9_100010_"

        base_url = 'https://steamcommunity.com/app/271590/homecontent/?'
        next_url = base_url + '&'.join([f'{key}={value}' for key, value in params.items()])

        yield scrapy.Request(url=next_url, headers={'Cookie': cookie}, callback=self.parse_page, meta={'index': i, 'cookie': cookie})

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SteamSpider)
    process.start()
