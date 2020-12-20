# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from scrapy_redis.spiders import RedisSpider
from sigo_shop_detail_spider import settings, spiderRedis
import json
import scrapy


class JDShopDetailSpider(RedisSpider):
    name = "shop_detail"
    
    headers = {}
    headers[":authority"] = "item.jd.com"
    headers[":method"] = "get"
    headers[":scheme"] = "https"
    headers["accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    headers["accept-encoding"] = "gzip, deflate, br"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    cookies = {}
    
    redis_key = "shop_queue"
    
    REDIS_URL = 'redis://@' + settings.REDIS_HOST + ':' + str(settings.REDIS_PORT)
    custom_settings = {
            'ITEM_PIPELINES':{'sigo_shop_detail_spider.pipelines.ShopDetailPipeline':300},
        }
    server = spiderRedis.redisClient

    def setup_redis(self, crawler=None):
        return RedisSpider.setup_redis(self, crawler=crawler)
    
    def start_requests(self):
        while True:
            shop_entry = self.server.brpop(self.redis_key)
            headers = self.headers.copy()
            shop_json = json.loads(shop_entry[1])["_values"]
            url = shop_json["url"]
            print(url)
            headers[":path"] = url[len("https://item.jd.com"):]
            yield scrapy.Request(url=shop_json["url"], callback=self.parse, headers=headers, cookies=self.cookies, cb_kwargs=shop_json)

    def parse(self, response, **kwargs):
        pass
        
