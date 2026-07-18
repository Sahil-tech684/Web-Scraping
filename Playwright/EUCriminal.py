import time
import pandas as pd
from playwright.sync_api import sync_playwright
from lxml import etree
def scrape():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        page = browser.new_page()
        page.goto('https://eumostwanted.eu/')
        res = etree.HTML(page.content())
        criminals = ['https://eumostwanted.eu' + i for i in res.xpath("//div[contains(@class,'wantedItem')]/@href") if i]
        data = []

        for criminal in criminals:
            page.goto(criminal)
            time.sleep(1)
            res = etree.HTML(page.content())

            data.append(
                {
                    'Name': res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'first-name')]/text()")[0],
                    'Country': res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'enfast-country')]/text()")[0].replace('by', '').strip() if res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'enfast-country')]/text()") else None,
                    'Crime': res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field-crime')]//div[@class='field__item']/text()")[0] if res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field-crime')]//div[@class='field__item']/text()") else None,
                    'Gender': res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field-gender')]//div[@class='field__item']/text()")[0] if res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field-gender')]//div[@class='field__item']/text()") else None,
                    'DOB': res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field field--node-field-date-of-birth field--name-field-date-of-birth field--type-datetime field--label-inline clearfix')]//div[@class='field__item']/time/text()")[0] if res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field field--node-field-date-of-birth field--name-field-date-of-birth field--type-datetime field--label-inline clearfix')]//div[@class='field__item']/time/text()") else None,
                    'Nationality': res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field-nationality')]//div[@class='field__item']/text()")[0] if res.xpath("//div[@class='wanted_top_right']/div[contains(@class, 'field-nationality')]//div[@class='field__item']/text()") else None,
                    'Background': '\n'.join([i.strip() for i in res.xpath("//div[@class='wanted_bottom_right']/div[contains(@class, 'field--type-text-with-summary')]/p//text()")])
                }
            )

            
        df = pd.DataFrame(data)
        df.to_csv('./30.0005.csv', index= False)


if __name__ == '__main__':
    scrape()