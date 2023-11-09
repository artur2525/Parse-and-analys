import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
from math import ceil
from random import randint
from time import sleep
from base64 import b64decode
from io import BytesIO
from PIL import Image
import pytesseract

from realty import check_database, create_table
from export import exporting
from config import CITY_OR_REGION
import re

URLs_AVITO = ['https://www.avito.ru/all/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?cd=1&f=ASgBAQECA0SeEu7XAYYUyOYB~vAP6Lv3AgRA4LYNZPaXKJyYKMqYKLSZKLiZKKKbMeK2DWSwoijuoijCpSiIrSjKrijkmzHqtg2UlMko0vAowPEoxPMozPkouP0ouv0ozpwx0Jwx8LYNNO63KPC3KPK3KAJF~AIXeyJmcm9tIjoyMDEwLCJ0byI6bnVsbH2~FRh7ImZyb20iOm51bGwsInRvIjoxNTUzNX0']


def avito_parser():
    #try:
    #    ua = UserAgent(use_cache_server=False,verify_ssl=False)
    #except FakeUserAgentError:
    ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    options = webdriver.FirefoxOptions()
    options.add_argument(f"user-agent={ua}")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Firefox(options=options)
    driver.implicitly_wait(15)
    
    
    for URL_AVITO in URLs_AVITO:
        driver.get(URL_AVITO)

        count = int(
            (
                driver.find_element(
                    by=By.CSS_SELECTOR, value='span[data-marker="page-title/count"]'
                ).text
            ).replace(" ", "")
        )

        print(count)
        reg = re.compile(r"[^\d\.]")
        for _ in range(10):
            offer = []
            elems = driver.find_elements(
                by=By.CSS_SELECTOR, value='div[data-marker="item"]'
            )
            
            for elem in elems:
                print(elem)
            
                avito_id = int(elem.get_attribute("id")[1:])
                print(avito_id)
                url = elem.find_element(
                    by=By.CSS_SELECTOR, value='a[itemprop="url"]'
                ).get_attribute("href")
                print(url)
                item_address = elem.find_element(
                    by=By.CSS_SELECTOR, value='span[class="styles-module-noAccent-nZxz7"]'
                ).text
                address = item_address
                print(address)
                oup = elem.find_element(
                    by=By.CSS_SELECTOR, value='a[itemprop="url"]'
                ).get_attribute("title").split(',')
                advert = oup[0]
                year = oup[1]
                race = oup[2].split('км')[0]
                race = reg.sub('', race)
                print(advert, year, race)

                price = elem.find_element(
                    by=By.CSS_SELECTOR, value='meta[itemprop="price"]'
                ).get_attribute("content")
                print(price)
                #rooms = 'kazan'#advert[0].split(", ")[0].split()[0].replace("-к.", "")
                #area = 'rio' #float(advert[0].split(", ")[1][:-3].replace(",", "."))
                #floor = int(advert[0].split(", ")[2].split("/")[0])
                #total_floor = int(advert[0].split(", ")[2].split("/")[1][:-4])
                #text = elem.find_element(
                #    by=By.CSS_SELECTOR, value='meta[itemprop="description"]'
                #).get_attribute("content")
                #online_display = "Да" if "Онлайн-показ" in advert else "Нет"

                #hover = ActionChains(driver).move_to_element(elem)
                #hover.perform()

                #button = elem.find_element(
                #    by=By.CSS_SELECTOR, value='button[type="button"]'
                #)
                #button.click()

                rand_sleep = randint(25, 49)
                sleep(rand_sleep / 10)

                #phone_pict = elem.find_element(
                #    by=By.CSS_SELECTOR, value="img[data-marker='phone-image']"
                #).get_attribute("src")
                #data = b64decode(phone_pict.split("base64,")[-1].strip())
                #image = Image.open(BytesIO(data))
                #phone_number = pytesseract.image_to_string(image).split("\n")[0]

                result = (
                    avito_id,
                    price,
                    advert,
                    year, 
                    race,
                    address,
                    url,
                )
                if '' not in result:
                    offer.append(result)
                print(result)
                
                
                
                
            check_database(offer)
            driver.find_element(
                by=By.CSS_SELECTOR, value='a[data-marker="pagination-button/nextPage"]'
            ).click()
    driver.quit()                               
            

if __name__ == "__main__":
    create_table()
    avito_parser()
    exporting()
