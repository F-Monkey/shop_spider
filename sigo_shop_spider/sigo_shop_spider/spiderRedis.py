'''
Created on 2020-12-18

@author: tangjianfei
'''
import redis
from sigo_shop_spider import settings

redis_pool = redis.ConnectionPool(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=3,decode_responses=True)

redisClient = redis.StrictRedis(connection_pool=redis_pool)