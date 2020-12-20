'''
Created on 2020-12-18

@author: tangjianfei
'''
from scrapy.crawler import CrawlerProcess
import sys
import os
from sigo_shop_detail_spider.spiders import JDShopDetailSpider
from selenium_spider.spider_redis import JDRedisMessageQueueHandler
from sigo_shop_detail_spider import spiderRedis

sys.path.append(os.getcwd())


if __name__ == '__main__':
    '''
    process = CrawlerProcess()
    process.crawl(JDShopDetailSpider)
    process.start()
    '''
    handler = JDRedisMessageQueueHandler(redis_key="shop_queue",redis_server=spiderRedis.redisClient)
    handler.start()
    