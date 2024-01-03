#%%
import pandas as pd
from tqdm import tqdm
from datetime import date
import pickle
import numpy as np
import time 

from selenium import webdriver
import requests
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait


#%%

#%%
#* real run
def convert_special_tokens_to_ascii(string):
    special_tokens = {
        '@': '%40',
        '"': '%22'
        # Add more special tokens and their corresponding ASCII values here if needed
    }
    
    converted_string = ''
    for char in string:
        if char in special_tokens:
            converted_string += special_tokens[char]
        else:
            converted_string += char
    
    return converted_string

def scrape_nitter(query, N = 200):
    driver = uc.Chrome(headless=False,use_subprocess=True)

    query = convert_special_tokens_to_ascii(query)
    driver.get('https://nitter.net/search?f=users&q='+query)

    people = []

    while len(people) < N:
        end = driver.find_elements(By.CLASS_NAME, "timeline-end")
        if len(end) > 0:
            break
        
        names = driver.find_elements(By.CLASS_NAME, "fullname")
        bios = driver.find_elements(By.CSS_SELECTOR, ".tweet-content")

        for name, bio in zip(names, bios):
            username = name.get_attribute('href')
            name = name.text
            
            bio = bio.text
            
            people.append({
                "username": username,
                "name": name,
                "bio": bio
            })
            
        print(people[-20:])
        
        show_more_div = driver.find_elements(By.CLASS_NAME, "show-more")[-1]
        
        show_more_link = show_more_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
        print(show_more_link)
        
        wait_time = np.random.randint(3, 7) + np.random.rand()
        print(wait_time)
        time.sleep(wait_time)
        
        driver.get(show_more_link)

    driver.quit()

    return people
#%%
queries = ["founder mit", "founder stanford", "founder harvard"]
schools = ["MIT", "Stanford", "Harvard"]

dfs = []
for i, query in enumerate(queries):
    people = scrape_nitter(query, N=1000)
    print(people)
    people_df = pd.DataFrame(people, columns=['username', 'name', 'bio'])
    people_df['school'] = schools[i]

    dfs.append(people_df)

merged = pd.concat(dfs, ignore_index=True)
merged.to_csv("final_nitter_scrapes.csv")

# %%
merged


# %%

#past code
driver = uc.Chrome(headless=True,use_subprocess=True)

driver.get('https://nitter.net/search?f=users&q=%22founder%22+harvard')

driver.implicitly_wait(2)

people = []

names = driver.find_elements(By.CLASS_NAME, "fullname")


#%%
#%%
options = uc.ChromeOptions()

ua = UserAgent()
user_agent = ua.random

options.add_argument(f'user-agent={user_agent}')

options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-gpu')
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920x1080")

driver = uc.Chrome(headless=False,use_subprocess=True, options = options)

driver.get('https://nitter.net/search?f=users&q=%22founder%22+harvard')
