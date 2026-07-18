import scrapy
from scrapy.crawler import CrawlerProcess

class GoodhereSpider(scrapy.Spider):
    name = "GoodHere"
    allowed_domains = ["goodhere.org"]
    start_urls = ["https://goodhere.org/organizations"]

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'GoodHereData.csv',
    }

    def parse(self, response):
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
        }

        links = response.css('div.border-gray-400 > a.flex::attr(href)').getall()
        for link in links:
            if '/organizations' not in link:
                url = 'https://goodhere.org/organizations' + str(link)
            else:
                url = 'https://goodhere.org' + str(link)
            yield scrapy.Request(url, callback=self.parse_page, headers=HEADERS)

    def parse_page(self, response):
        all_li_elements = response.css('li')
        filter_Org_work = [li for li in all_li_elements if li.css('svg[data-icon="box"]')]
        filter_Org_Type = [li for li in all_li_elements if li.css('svg[data-icon="building"]')]
        filter_Org_link = [li for li in all_li_elements if li.css('svg[data-icon="external-link-alt"]')]
        filter_Org_Emp = [li for li in all_li_elements if li.css('svg[data-icon="users"]')]

        yield {
            'Name': response.css('div.mr-2 > h1.flex-grow::text').extract_first(default=None),
            'Descp1': response.css('div.mr-2 > p::text').extract_first(default=None),
            'Descp2': response.css('div.my-6::text').extract_first(default=None),
            'Org_Work': [li.css('span::text').get() for li in filter_Org_work] if filter_Org_work else None,
            'Org_Type': [li.css('span::text').get() for li in filter_Org_Type] if filter_Org_Type else None,
            'Org_link' : [li.css('a::attr(href)').get() for li in filter_Org_link] if filter_Org_link else None,
            'Num_of_Emp' : [li.css('span::text').get() for li in filter_Org_Emp] if filter_Org_Emp else None,
        }

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Avast/117.0.0.0',
    })
    process.crawl(GoodhereSpider)
    process.start()
