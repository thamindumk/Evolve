# import scrapy
# from services.scrapeService import getShopId

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from ..items import WebscrapingItem
import time


class CherriSpider(CrawlSpider):
    # def __int__(self):
    #     self.shopId = getShopId()

    name = "cherri"
    start_urls = [
        "https://cherri.lk/home",
    ]

    rules = [
        Rule(LinkExtractor(allow=r"lk/products/[Women|Men|Kids]", deny="mcat=")),
        Rule(LinkExtractor(allow=r"/clothes/"), callback="parse_item", follow=True)
    ]

    def parse_item(self, response):
        time.sleep(0.3)
        items = WebscrapingItem()

        title = response.css('.p24::text').get()
        description = response.css('.p20+ p').css('::text').get()
        price = response.css('.hidden-xs > .p18').css('::text').extract()
        images = response.css('.xzoom-gallery5::attr(src)').extract()
        sizes = response.css('.sizeBtn').css('::text').extract()
        cleaned_sizes = [size.strip() for size in sizes if size.strip()]
        items['title'] = title
        items['description'] = description
        items['price'] = price[-1]
        items['images'] = images
        items['sizes'] = cleaned_sizes
        items['link'] = response.request.url
        items['availability'] = True if len(sizes) > 0 else False
        items['shop_name'] = "cherri"

        yield items
