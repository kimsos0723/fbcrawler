
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException

import time 
from bs4 import BeautifulSoup as BSoup
from .nlp import analyze
# from nlp import analyze
class Post:
    def __init__(self, poster_name: str, mentioned_names: list, imgs: list, texts: list):
        self.poster_name = poster_name
        self.mentioned_names = mentioned_names
        self.imgs = imgs
        self.texts = texts
        self.analy = []
        for t in texts:
           self.analy.append(analyze(t))
        self.analyzed_text = zip(self.texts, self.analy)
class Friend:
    def __init__(self, friend_id,friend_name):
        self.id = friend_id        
        self.name = friend_name
        print('id', self.id)

    def GET_post(self, driver: webdriver.Chrome):
        url = 'https://www.facebook.com/' + self.id
        time.sleep(3)
        driver.get(url)      
        time.sleep(3)            
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")                
        for _ in range(5) :        
            # Scroll down to bottom            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
     
        
        for a in driver.find_elements_by_class_name('showAll._5q5v'):
            try:
                a.click()
            except Exception as e:
                print(e)
                pass

        post_elem = driver.find_elements_by_class_name("_1dwg._1w_m._q7o")  
        post_list = []      
        for post in post_elem:
            # see more link 
            try:
                see_more = post.find_element_by_class_name('see_more_link')
                driver.execute_script('arguments[0].click();',see_more)
                time.sleep(0.5)
            except:
                pass
            # names 
            names = []            
            post_bs = BSoup(post.get_attribute('innerHTML'), 'html5lib')
            fwn_fcgs = post_bs.find_all('span',class_="fwb fcg")
            for fwn_fcg in fwn_fcgs: 
                for a in fwn_fcg.find_all('a'):
                    names.append(a.get_text())
            if (names == []):
                pass
            if any(elem == '' for elem in names):
                pass
            # imgs 
            img_list = [img['src'] for img in post_bs.find_all('img')]
            # post_elem
            text_list = []
            for div in post_bs.find_all('div', {"data-testid" : "post_message"}):
                if(div.text == []):
                    pass
                text_list.append(div.text)
            if( not text_list ):
                pass
            print(text_list)
            print("===========================================================\n")            
            post_list.append(Post(self.name, names, img_list, text_list))
        return post_list
        