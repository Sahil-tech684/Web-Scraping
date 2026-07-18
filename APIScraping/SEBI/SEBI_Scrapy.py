import scrapy
from scrapy.crawler import CrawlerProcess

class SEBISpider(scrapy.Spider):
    name = "SEBI"
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'SEBI_Data_1.csv',
        'CONCURRENT_REQUESTS': 32,
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.sebi.gov.in',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        for page in range(464, 466):
            yield scrapy.Request(
                url='https://www.sebi.gov.in/sebiweb/ajax/home/getnewslistinfo.jsp',
                method='POST',
                body=f'nextValue=1&next=n&search=&fromDate=&toDate=&fromYear=&toYear=&deptId=-1&sid=2&ssid=50&smid=0&ssidhidden=50&intmid=-1&sText=Enforcement&ssText=Recovery Proceedings&smText=&doDirect={page-1}',
                callback=self.parse_result_page,
                headers=self.headers
            )

    def parse_result_page(self, response):
        for row in response.css("table[role='grid'] tr")[1:]:
            yield scrapy.Request(
                url=row.css("td:nth-child(2) a::attr(href)").get(),
                headers=self.headers,
                callback=self.parse_pdf,
                meta={
                    'date': row.css("td:nth-child(1)::text").get().replace('  ', '').strip().replace('\n', '') if row.css("td:nth-child(1)::text").get() is not None else None,
                    'title': row.css("td:nth-child(2) a::text").get().replace('  ', '').strip().replace('\n', '') if row.css("td:nth-child(2) a::text").get() is not None else None
                }
            )

    def parse_pdf(self, response):
        url = response.css("iframe::attr(src)").get().split('?file=')[-1] if response.css("iframe::attr(src)").get() is not None and '.pdf' in response.css("iframe::attr(src)").get() else response.url
        yield {
            'Date': response.meta['date'],
            'Title': response.meta['title'],
            'PDF URL': 'https://www.sebi.gov.in' + url if 'https://www.sebi.gov.in' not in url else url
        }

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SEBISpider)
    process.start()