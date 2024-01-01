from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd 
import constant as const

def init_driver(url):
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver

cnt = 0

SCROLL_PAUSE_TIME = 1.5
url_list = list()
df = pd.DataFrame(columns=["url"]) # boş bir DataFrame oluştur
def getUrl(driver):

    while True:
        try:
            html_part = driver.execute_script("return document.querySelector('.css-1yt392s').innerHTML") # Sayfanın sadece belirli bir bölümünü al
            soup = BeautifulSoup(html_part, "html.parser") # kaynağı al ve BeautifulSoup ile parse et
            links = soup.find_all('a')
            
            # gelen linkleri ekrana yazdır
            for link in links:
                url = link.get('href')
                if url is not None and "/tr/feed/post" in url and url not in url_list:
                    url_list.append(url)
            df = pd.DataFrame(url_list,columns=["url"]) # url_list'teki verileri DataFrame'e dönüştür
            df.to_excel("url.xlsx", index=False) # DataFrame'i Excel dosyasına kaydet
            print(f"\r---------{len(url_list)}-----------", end='', flush=True)       
            # Sayfa en altına kaydır
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
            if(len(url_list) > 2000):
                break
        except:
            print("Hata oluştu")
            df = pd.DataFrame(url_list) # data_list'teki verileri DataFrame'e dönüştür
            df.to_excel("url.xlsx", index=False)

            




