from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import binanceData as bd 
import constant as const

def init_driver(url):
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver


def loading_bar(currentValue,length):
    print(f"\r---------{currentValue} / {length-1}-----------", end='', flush=True)
   
    

SCROLL_PAUSE_TIME = 3
cnt = 0
url_list = list()
df = pd.DataFrame(columns=["url", "title", "content","symbol","indexPrice","date"]) # boş bir DataFrame oluştur


driver = init_driver(const.binance_feed_url)
time.sleep(5)
while True:
    html_part = driver.execute_script("return document.querySelector('.css-1yt392s').innerHTML") # Sayfanın sadece belirli bir bölümünü al
    soup = BeautifulSoup(html_part, "html.parser") # kaynağı al ve BeautifulSoup ile parse et
    links = soup.find_all('a')
    
    # gelen linkleri ekrana yazdır
    for link in links:
        url = link.get('href')
        if url is not None and "/tr/feed/post" in url:
            url_list.append(url)
            print(url)

    # Sayfa en altına kaydır
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    cnt += 1
    
    # Belirli bir sayıda kaydırmadan sonra dur
    if cnt == 1:
        break
    
    time.sleep(SCROLL_PAUSE_TIME)


json_data = list()
data_list = []

for index, url in enumerate(url_list):
    #loading_bar(index, len(denemeSet))
    newUrl = const.binance_url + url
    try:
        driver.execute_script(f"window.open('{newUrl}', '_self');")
        time.sleep(2)
        html_content = driver.execute_script("return document.documentElement.innerHTML")
        soup = BeautifulSoup(html_content, "html.parser")
        
        title = soup.find('h1').text
        content = soup.find('div', id="articleBody").text
        
        symbols_list = []
        indexPrice_list = []
        try:
            symbols = soup.find_all('span', class_='symbol')
            indexPrice = soup.find_all('span', class_='index price-decline')
            date = soup.find('div', class_='date').text
            print(date)
            for index in indexPrice:
                indexPrice_list.append(index.text)
            for symbol in symbols:
                symbols_list.append(symbol.text)
        except:
            symbols_list.append("None")
        data = bd.binanceData(newUrl,title,content,symbols_list,indexPrice_list,date)
        data_list.append(data.to_dict())  # sözlük olarak ekle
        
    except requests.exceptions.RequestException as e:
        print("Geçersiz URL veya bağlantı hatası:", e)
        
driver.quit()

df = pd.DataFrame(data_list) # data_list'teki verileri DataFrame'e dönüştür
df.to_excel(const.file_name, index=False) # DataFrame'i Excel dosyasına kaydet


