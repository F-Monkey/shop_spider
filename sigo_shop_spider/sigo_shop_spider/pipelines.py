# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from sigo_shop_spider.spiderRedis import redisClient


class SigoShopSpiderPipeline:
    def process_item(self, item, spider):
        return item

class JDShopPipeline(SigoShopSpiderPipeline):
    '''
     send data to redis
    '''    
    redis_key = "shop_queue"
    
    def process_item(self, item, spider):
        item_json = json.dumps(item.__dict__)
        print(item_json)
        redisClient.lpush(self.redis_key,item_json)