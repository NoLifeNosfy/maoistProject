import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

class Sele:
    def __init__(self):
        # 创建浏览器对象
        self.options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(options=self.options)

        # 获取待访问的网址
        self.browser.get("https://poe.com")

        self.cookies = [
            {"domain": "poe.com", "expirationDate": 1727936950.759125, "hostOnly": True, "httpOnly": True,
             "name": "p-b",
             "path": "/", "sameSite": "None", "secure": True, "session": False, "storeId": "0",
             "value": "1ro3F3D7bLgi0LNLsl9j8g%3D%3D"},
            {"domain": ".poe.com", "expirationDate": 1724911342.436477, "hostOnly": False, "httpOnly": True,
             "name": "cf_clearance", "path": "/", "sameSite": "None", "secure": True, "session": False, "storeId": "0",
             "value": "mOe1m65scaeYI1IiNa81i1oVfvL5_s3.5lyCvL.NiJA-1693375340-0-1-8df0164b.2a495901.daf149ab-0.2.1693375340"},
            {"domain": ".poe.com", "expirationDate": 1693378750.75916, "hostOnly": False, "httpOnly": True,
             "name": "__cf_bm", "path": "/", "sameSite": "None", "secure": True, "session": False, "storeId": "0",
             "value": "em.J.03dhbnoL0Av5B7QWJ1374B5L1b7gC3SOeAd.Hg-1693376949-0-AfpD2PguBTWBEVqTmgEkka20yDAbyxNaS958lZHrgyHcqGGYdw+cmFKiJJuB4+yp9/UD5ifWTcugYuIe8bPkrRc="}]

        for cookie in self.cookies:
            self.browser.add_cookie(cookie)

        self.browser.get("https://poe.com/Assistant")

        '''
            1.打开网页，将浏览器调整为开发者模式
            2.找到需要操作的地方对应的代码
            3.例如这里是根据id来执行操作的
        '''

        # browser.find_element(By.ID,"kw").send_keys("hello world")
        # browser.find_element(By.ID,"su").click()


    def getEmoFromSele(self, str):
        prompt = """Given a raw Chinese text input, Judge the emotions contained in this text. Your output should follow the following format: "({1}, {2}), ({3}, {4})..."
{1} represent for the first emotion. {2} represent for the weight value of emotion1.
{3} represent for the second emotion. {4} represent for the weight value of emotion2.
and then other emotions.
Don't output any other words.

here's 2 examples:
example 1
<<input>>:
你好，我今天很开心。
<<output>>:
(happiness, 0.6), (glad, 0.3), (welcome, 0.1)

example 2
<<input>>:
对生活感到很失望，感觉前途很迷茫。
<<output>>:
(disappointed, 0.5), (confused, 0.3), (sad, 0.1)


now judge the emotions of the following input.  Don't output extra information."""
        strs = prompt.split("\n")
        for s in strs:
            self.browser.find_element(By.CLASS_NAME, "GrowingTextArea_textArea__eadlu").send_keys(s)
            ActionChains(driver=self.browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).perform()
            ActionChains(driver=self.browser).key_up(Keys.SHIFT).perform()


        self.browser.find_element(By.CLASS_NAME, "GrowingTextArea_textArea__eadlu").send_keys("<<input>>:")
        ActionChains(driver=self.browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).perform()
        self.browser.find_element(By.CLASS_NAME, "GrowingTextArea_textArea__eadlu").send_keys(str)
        ActionChains(driver=self.browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).perform()
        self.browser.find_element(By.CLASS_NAME, "GrowingTextArea_textArea__eadlu").send_keys("<<output>>:")
        ActionChains(driver=self.browser).key_down(Keys.SHIFT).key_down(Keys.ENTER).perform()
        ActionChains(driver=self.browser).key_up(Keys.SHIFT).key_down(Keys.ENTER).perform()
        time.sleep(20)

        elements = self.browser.find_elements(By.CLASS_NAME, "Markdown_markdownContainer__UyYrv")
        return elements[-1].text


if __name__ == '__main__':
    sele = Sele()


    print(sele.getEmoFromSele("who are you?"))