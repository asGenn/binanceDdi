from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import binanceData as bd
import constant as const
import getUrl as gu


def init_driver(url):
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    return driver


def loading_bar(currentValue, length):
    print(f"\r---------{currentValue} / {length -
          1}-----------", end='', flush=True)


SCROLL_PAUSE_TIME = 3
# boş bir DataFrame oluştur
df = pd.DataFrame(columns=["url", "title", "content",
                  "symbol", "indexPrice", "date"])


driver = init_driver(const.binance_feed_url)


json_data = list()
data_list = []

# gu.getUrl(driver)
# Excel dosyasından url'leri oku
url_list = pd.read_excel("url.xlsx", usecols="A")
# data_list = pd.read_excel("veriler4.xlsx").values.tolist # Excel dosyasından verileri oku
starIndex = 615
for index, url in enumerate(url_list["url"][starIndex:], start=starIndex):
    loading_bar(index, len(url_list["url"]))
    newUrl = const.binance_url + url
    print(newUrl)
    try:
        driver.execute_script(f"window.open('{newUrl}', '_self');")
        time.sleep(2)

        symbols_list = []
        indexPrice_list = []
        try:
            html_content = driver.execute_script(
                "return document.documentElement.innerHTML")
            soup = BeautifulSoup(html_content, "html.parser")
            title = soup.find('h1').text
            content = soup.find('div', id="articleBody").text
            symbols = soup.find_all('span', class_='symbol')
            indexPriceRaise = soup.find_all('span', class_='index price-raise')
            indexPriceDecline = soup.find_all(
                'span', class_='index price-decline')
            date = soup.find('div', class_='date').text
            for index in indexPriceRaise:
                indexPrice_list.append(index.text)
            for index in indexPriceDecline:
                indexPrice_list.append(index.text)
            for symbol in symbols:
                symbols_list.append(symbol.text)

        except Exception as e:
            driver.quit()
            driver = init_driver(const.binance_feed_url)
            print(e)
            # symbols_list.append("None")
        try:
            data = bd.binanceData(newUrl, title, content,
                                  symbols_list, indexPrice_list, date)
            data_list.append(data.to_dict())  # sözlük olarak ekle
            # data_list'teki verileri DataFrame'e dönüştür
            df = pd.DataFrame(data_list)
            # DataFrame'i Excel dosyasına kaydet
            df.to_excel("veriler5.xlsx", index=False)

        except:
            print("Hata oluştu")

    except requests.exceptions.RequestException as e:
        print("Geçersiz URL veya bağlantı hatası:", e)

driver.quit()
