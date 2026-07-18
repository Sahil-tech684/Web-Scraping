import scrapy
from urllib.parse import quote
from scrapy.crawler import CrawlerProcess

class SteamReviewSpider(scrapy.Spider):
    name = "SteamReview"

    BASE_URL = 'https://steamcommunity.com/app/'
    URL_TAIL = '&numperpage=10&browsefilter=toprated&l=english&appHubSubSection=10&filterLanguage=default&searchText=&maxInappropriateScore=50&forceanon=1'

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67',
    }

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'GTA_reviews_sample.json',
        # 'LOG_LEVEL': 'ERROR'
    }

    def start_requests(self):
        url = f'{self.BASE_URL}271590/homecontent/?userreviewsoffset=0&p=1&workshopitemspage=1&readytouseitemspage=1&mtxitemspage=1&itemspage=1&screenshotspage=1&videospage=1&artpage=1&allguidepage=1&webguidepage=1&integratedguidepage=1&discussionspage=1{self.URL_TAIL}'
        yield scrapy.Request(url=url, headers=self.HEADERS, callback=self.parse_reviews, meta={'index': 0, 'cookie': 'app_impressions='})

    def parse_reviews(self, response):
        for review in response.css("div.apphub_Card.modalContentLink.interactable"):
            review_txt = '\n'.join(review.css("div.apphub_CardTextContent::text").getall()).strip()
            if not review_txt:
                temp = [i.strip() for i in review.css("div.apphub_CardTextContent::text").getall()]
                review_txt = '\n'.join([i for i in temp if 'Posted:' not in i and 'Product received for free' != i]).strip()

            yield {
                'user_name': review.css("div.apphub_CardContentAuthorName a::text").get(),
                'user_profile_url': review.css("div.apphub_CardContentAuthorName a::attr(href)").get(),
                'user_acount_info': review.css("div.apphub_CardContentMoreLink::text").get(),
                'found': [i.strip() for i in review.css("div.found_helpful::text").getall()[:-1]],
                'review_award_count': review.css("div.review_award_aggregated.tooltip::text").get(),
                'hours_count': review.css("div.reviewInfo span.hours::text").get(),
                'title': review.css("div.reviewInfo span.title::text").get(),
                'date_posted': review.css("div.date_posted::text").get().split(': ')[-1],
                'received_compensation': review.css("div.received_compensation::text").get(),
                'comment_count': review.css("div.apphub_CardCommentCount::text").get().replace(',', ''),
                'review': review_txt,
            }


        cursor = quote(response.css("input[name='userreviewscursor']::attr(value)").get())
        i = response.meta['index'] + 1
        cookie = f"{response.meta['cookie']}|730@2_9_100010_" if i else f"{response.meta['cookie']}730@2_9_100010_"

        url = f"{self.BASE_URL}271590/homecontent/?userreviewscursor={cursor}&userreviewsoffset={i*10}&p={i+1}&workshopitemspage={i+1}&readytouseitemspage={i+1}&mtxitemspage={i+1}&itemspage={i+1}&screenshotspage={i+1}&videospage=1&artpage={i+1}&allguidepage={i+1}&webguidepage={i+1}&integratedguidepage={i+1}&discussionspage={i+1}{self.URL_TAIL}"

        yield scrapy.Request(url=url, headers={'Cookie': cookie}, callback=self.parse_reviews, meta={'index': i, 'cookie': cookie})

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SteamReviewSpider)
    process.start()
