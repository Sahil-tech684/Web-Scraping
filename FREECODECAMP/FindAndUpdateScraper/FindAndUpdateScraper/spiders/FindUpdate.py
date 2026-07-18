import scrapy

class FindupdateSpider(scrapy.Spider):
    name = "FindUpdate"
    base_url = 'https://goodhere.org/organizations'
    
    def parse(self, response):
        links = response.css('div.border-gray-400 > a.flex::attr(href)').getall()
        for link in links:
            url = 'https://goodhere.org' + str(link)
            yield scrapy.Request(url, callback=self.parse_page)
        
    def parse_page(self, response):
        Org_info = response.css('div.flex.flex-col.mb-8')
        yield {
            'Name': response.css('div.mr-2 > h1.flex-grow::text').extract_first(default=None),
            'Descp1': response.css('div.mr-2 > p::text').extract_first(default=None),
            'Descp2': response.css('div.my-6::text').extract_first(default=None),
            'Category': Org_info[0].css('li.mt-3 span::text').extract_first(default=None),
            'Finance' : Org_info[0].css('div.inline-flex span::text').extract_first(default=None),
            'Link' : Org_info[1].css('li.mt-3 a.underline::attr(href)').extract_first(default=None),
        }