# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_names != 'Description':
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        value = adapter.get('Price')
        value = value.replace('£','')
        adapter['Price'] = float(value)

        availability_string = adapter.get('Availability')
        match = re.search(r'\d+', availability_string)    # Extract the number from the 'Availability' string
        if match:
            number = int(match.group())
            adapter['Availability'] = number
        
        Rating_string = adapter.get('Rating')
        Split_Rating_string = Rating_string.split(' ')
        Rating_text = Split_Rating_string[1].lower()
        if Rating_text == 'zero':
            adapter['Rating'] = 0
        elif Rating_text == 'one':
            adapter['Rating'] = 1
        elif Rating_text == 'two':
            adapter['Rating'] = 2
        elif Rating_text == 'three':
            adapter['Rating'] = 3
        elif Rating_text == 'four':
            adapter['Rating'] = 4
        elif Rating_text == 'five':
            adapter['Rating'] = 5


        return item
