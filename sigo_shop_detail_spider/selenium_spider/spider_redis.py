'''
Created on 2020-12-19

@author: tangjianfei
'''
import redis
import json
from telnetlib import EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from pip._vendor.urllib3.util import url
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from sigo_shop_detail_spider import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SimpleRedisMsgQueueHandler():
    def __init__(self,redis_key:str,redis_server:redis.StrictRedis):
        self.redis_key = redis_key
        self.redis_server = redis_server
        
    def start(self):
        self.__execute_loop__()
        
    def __execute_loop__(self):
        while True:
            val = self.redis_server.brpop(self.redis_key)
            self.execute(val)
    def execute(self,val:str):
        raise "must implemented"


class Driver():
    
    def __wait__(self, type_, value, waitTime=None):
        wait = waitTime if waitTime else self.waitTime
        locator = (type_, value)
        WebDriverWait(self.browser, wait, self.waitFrequency).until(EC.presence_of_element_located(locator))
        
    def __init__(self, waitTime=None, waitFrequency=None, forbidden_pic=False, forbidden_js=False, headless=False):
        self.waitTime = waitTime if waitTime else 20;
        self.waitFrequency = waitFrequency if waitFrequency else 0.5
        
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = { 'performance':'ALL' }

        chrome_options = webdriver.ChromeOptions()
        prefs = {
                'profile.default_content_setting_values':{
                        'images':2 if forbidden_pic else 1,
                        'javascript': 2 if forbidden_js else 1
                    }
            }
        chrome_options.add_experimental_option('prefs', prefs)
        if headless:
            chrome_options.add_argument('headless')
        self.browser = webdriver.Chrome(executable_path = settings.CHROME_DIRVER_PATH,chrome_options=chrome_options)

    def find(self, by, value, need_wait=True):
        if need_wait :
            self.__wait__(by, value)
        return self.browser.find_elements(by, value)

    def get_page_source(self):
        return self.browser.page_source
    
    def move_to_element(self,element:WebElement):
        ActionChains(self.browser).move_to_element(element)
        
    def get_network_resource(self):
        return self.browser.get_log("performance")
    
    
class JDRedisMessageQueueHandler(SimpleRedisMsgQueueHandler,Driver):
    
    def __init__(self,redis_key:str,redis_server:redis.StrictRedis):
        SimpleRedisMsgQueueHandler.__init__(self, redis_key, redis_server)
        Driver.__init__(self)
        self.img_xpath = "//*[@id=\"spec-list\"]/ul/li"
        self.big_img_xpath = "//*[@id=\"spec-img\"]"
        
    def execute(self,tuple:tuple):
        shop_json = json.loads(tuple[1])["_values"]
        url = shop_json["url"]
        self.browser.get(url)
        big_img_element = self.find(By.XPATH,self.big_img_xpath)[0]
        big_img_list = []
        for img_element in self.find(By.XPATH, self.img_xpath):
            self.move_to_element(img_element)
            self.move_to_element(big_img_element)
            # find network resource
            network_resources = self.get_network_resource()
            if network_resources and len(network_resources) > 0:
                big_img_list.append(network_resources[len(network_resources) -1])
        self.browser.close()