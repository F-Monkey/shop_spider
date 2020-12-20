'''
'''
from selenium.webdriver.chrome.webdriver import WebDriver
from sigo_shop_detail_spider import settings
import threading

class ShopImgHandler(threading.Thread):
    def __init__(self,barrier):
        if not self.driver:
            self.driver = WebDriver(executable_path = settings.CHROME_DIRVER_PATH)
            self.barrier = barrier
    def run(self):
        while True:
            try:
                self.execute()
            finally:
                self.barrier.wait()
            
    def execute(self):
        raise "must implemented"

class JDShopImgHandler(ShopImgHandler):
    def __init__(self,barrier,taskQueue,resultQueue):
        ShopImgHandler.__init__(self, barrier)
        self.taskQueue = taskQueue
        self.resultQueue = resultQueue
    
    def run(self):
        while len(self.taskQueue) > 0:
            try:
                self.execute()
            finally:
                self.barrier.wait()
    
    def execute(self):
        pass