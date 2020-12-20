# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import scrapy

from scrapy.spiders import Spider
from sigo_shop_spider import settings, spiderRedis
import json
from sigo_shop_spider.items import ShopItem
from scrapy_redis.spiders import RedisSpider


class JDShopSpider(scrapy.Spider):
    name = "jd"
    
    def __init__(self):
        self.keyword = settings.KEY_WORD
        
    root_url = settings.SHOPS_DICT["JD"]
    
    custom_settings = {
            'ITEM_PIPELINES':{'sigo_shop_spider.pipelines.JDShopPipeline':300},
        }
    MAX_DEEP_INDEX = 3
        
    def start_requests(self):
        for i in range(0, self.MAX_DEEP_INDEX, 1):
            url = self.root_url.replace("{keyword}", self.keyword).replace("{page}", str(i))
            yield scrapy.Request(url=url, method='get', callback=self.parse)
    
    def parse(self, response, **kwargs):
        if response.status == 200:
            text = response.text
            text = text[len("jQuery7406156("):-1]
            json_dict = json.loads(text)
            for key in json_dict:
                shop_list = json_dict[key]
                for shop_json in shop_list:
                    shop = ShopItem()
                    shop["name"] = shop_json["shop_link"]["shop_name"]
                    shop["id"] = shop_json["shop_id"]
                    shop["url"] = shop_json["link_url"]
                    yield shop
