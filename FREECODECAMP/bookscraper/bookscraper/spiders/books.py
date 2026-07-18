import scrapy
from bookscraper.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            relative_url = book.css('h3 a::attr(href)').get()

            if 'catalogue/' in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

        for page in range(2,51):
            next_page_url = 'https://books.toscrape.com/catalogue/page-'+str(page)+'.html'
            yield response.follow(next_page_url, callback= self.parse)
    
    def parse_book_page(self, response):
        table_rows = response.css('table tr')
        book_item = BookItem()
        
        book_item['Title'] = response.css('div.col-sm-6.product_main h1::text').get(),
        book_item['Rating'] =  response.css('p.star-rating').attrib['class'],
        book_item['Description'] = response.css('article.product_page > p::text').get(),
        book_item['Availability'] = table_rows[5].css('td::text').get(),
        book_item['Price'] = table_rows[3].css('td::text').get(),
        book_item['Url'] = response.url,   

        yield book_item