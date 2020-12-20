'''
Created on 2020-12-18

@author: tangjianfei
'''
from scrapy.crawler import CrawlerProcess
import sys
import os
from sigo_shop_spider.spiders import JDShopSpider

sys.path.append(os.getcwd())


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(JDShopSpider)
    #process.crawl(JDShopDetailSpider)
    process.start()