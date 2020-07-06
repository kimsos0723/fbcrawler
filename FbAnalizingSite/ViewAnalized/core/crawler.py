import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from friends import Friend
from .friends import Friend
import json
import pprint
from bs4 import BeautifulSoup as BSoup

def make_driver() : 
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("lang=ko_KR")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')


    prefs = {'profile.default_content_setting_values': { 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver

def close_driver(driver: webdriver.Chrome) :
    driver.close()

def GET_friends ( id:str, pw:str, driver:  webdriver.Chrome) :    

    elem = driver.find_element_by_xpath('//*[@id="email"]')
    elem.send_keys(id)
    elem = driver.find_element_by_xpath('//*[@id="pass"]')
    elem.send_keys(pw)
    elem.send_keys(Keys.RETURN)
    # return
    # GET FRIENDS LIST
    time.sleep(0.5)
    driver.get('https://www.facebook.com/me/friends')
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(4):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(1)
        
    # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height        
        
    friend_list = {}
    page_source = driver.page_source
    page = BSoup(page_source, 'html5lib')
    for i in page.find_all('div', class_ = 'fsl fwb fcb'):
        data_gt = i.find('a', {'data-gt' :  True})
    # for i in driver.find_elements_by_class_name('fsl.fwb.fcb'):
    #     a = i.find_element_by_css_selector('a')    
    #     data_gt = a.get_attribute('data-gt')            
        if data_gt:
            json_data = json.loads(data_gt['data-gt'])            
            # friend_list.append({i.text : json_data['engagement']['eng_tid']})
            friend_list.update({i.text : json_data['engagement']['eng_tid']})
        else:             
            pass    
    return friend_list


if __name__ == "__main__":    
    driver = make_driver()    
    driver.get('https://www.facebook.com')
    try:
        friends = GET_friends('FB ID', 'FB PW',driver)
        print(friends)
        Friend('100006481061584','유동근').GET_post(driver)
    except Exception as e:
        print(e)
    finally:            
        close_driver(driver)