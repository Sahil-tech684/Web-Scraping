import scrapy


class FsrascraperSpider(scrapy.Spider):
    name = "FSRAScraper"
    allowed_domains = ["teao.fsrao.ca"]
    star_url = ['https://teao.fsrao.ca/?searchRequired=true&searchText=&enfActions=false&warnings=false&hasRelatedFiles=false&selectedStatus=0&startDate=&endDate=']

    def parse(self, response):
        
        pass
