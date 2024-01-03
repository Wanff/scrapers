#%%
from selenium import webdriver
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import pandas as pd
from tqdm import tqdm
from datetime import date
import pickle
import numpy as np

def create_driver():
    options = Options()
    # options.headless = True
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--disable-gpu')
    options.add_argument("--no-sandbox")

    chrome_prefs = {}
    options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    driver = webdriver.Chrome(options = options)
    print("driver successfully created")
    return driver





#%%
import undetected_chromedriver as uc
from fake_useragent import UserAgent

ua = UserAgent()
user_agent = ua.random

opts = uc.ChromeOptions()

# opts.add_argument(f'user-agent={user_agent}')
# opts.add_argument( f'--proxy-server=15.237.84.201' )

driver = uc.Chrome(headless=False,use_subprocess=True, options = opts)

# driver.get('https://nowsecure.nl')
# driver.save_screenshot('nowsecure.png')

driver.get('https://twitter.com')
driver.save_screenshot('twitter.png')


#%%


# %%
from selenium.webdriver.common.by import By

def get_free_proxies(driver):
    driver.get('https://sslproxies.org')

    table = driver.find_element(By.TAG_NAME, 'table')
    thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
    tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    headers = []
    for th in thead:
        headers.append(th.text.strip())

    proxies = []
    for tr in tbody:
        proxy_data = {}
        tds = tr.find_elements(By.TAG_NAME, 'td')
        for i in range(len(headers)):
            proxy_data[headers[i]] = tds[i].text.strip()
        proxies.append(proxy_data)
    
    return proxies

free_proxies = get_free_proxies(driver)

print(free_proxies)
# %%
