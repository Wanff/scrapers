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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from dotenv import load_dotenv

# %%
load_dotenv()
# %%
driver = uc.Chrome(headless=False,use_subprocess=True)
driver.implicitly_wait(10)

driver.get('https://linkedin.com')

people = []
query = "founder MIT"
N = 500

#*login
email = driver.find_element(By.ID, "session_key")
email.send_keys(os.getenv("EMAIL"))

time.sleep(np.random.rand())

pw = driver.find_element(By.ID, "session_password")
pw.send_keys(os.getenv("PASSWORD"))

time.sleep(np.random.rand())

sign_in_button = driver.find_element(By.CLASS_NAME, "sign-in-form__submit-btn--full-width")
sign_in_button.click()

time.sleep(2 + np.random.rand())

#* query
# search-global-typeahead__collapsed-search-button
search = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")
search.send_keys(query)
search.send_keys(Keys.RETURN)

time.sleep(2 + np.random.rand())

driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 20);")
time.sleep(np.random.rand())

see_all_results = driver.find_elements(By.CLASS_NAME, "search-results__cluster-bottom-banner")[0]
wait = WebDriverWait(driver, 10)
wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search-results__cluster-bottom-banner")))
see_all_results.click()

time.sleep(1 + np.random.rand())

#* scrape profiles

people = []
buttons_clicked = 1
while len(people) < N:
    profiles = driver.find_elements(By.CLASS_NAME, "reusable-search__result-container")
    subtitles = driver.find_elements(By.CLASS_NAME, "entity-result__primary-subtitle")

    for profile, subtitle in zip(profiles, subtitles):
        
        links = profile.find_elements(By.CLASS_NAME, "app-aware-link")
        url_tag = links[1]
        
        # try:
        #     img = url_tag.find_element(By.TAG_NAME, "img")
        #     name = img.get_attribute("alt")
        # except:
        #     print(url_tag.get_attribute('innerHTML'))
        #     name = ""
        span1 = url_tag.find_element(By.TAG_NAME, "span")
        name = span1.find_elements(By.TAG_NAME, "span")[0].text
        # name = url_tag.find_element(By.XPATH, '/span/span[1]').text
        
        linkedin_url = url_tag.get_attribute('href').split("?")[0]
        subtitle = subtitle.text
        
        people.append({
            'name': name,
            'linkedin_url': linkedin_url,
            'subtitle': subtitle
        })
    
    print(people)
    
    time.sleep(np.random.rand())
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(np.random.rand())
    
    button_lis = driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator")
    button = None
    for button_li in button_lis:
        temp_button = button_li.find_element(By.TAG_NAME, "button")
        #this gets the aria-label attribute which is PAGE NUM, and then matches it to what button we're supposed to click
        if temp_button.get_attribute("aria-label").split("Page ")[1] == str(buttons_clicked + 1):
            button = temp_button
            print("Found Button " + str(buttons_clicked + 1))
            break

    if button is not None:
        button.click()
    else:
        print("Button not found")

    buttons_clicked += 1
    time.sleep(2 + np.random.rand())
    
print(people)

driver.quit()
# %%


#%%
people_df = pd.DataFrame(people, columns=['name', 'linkedin_url', 'subtitle'])
# people_df.columns = ['name', 'usern', 'subtitle']
people_df['school'] = "MIT"
people_df.to_csv("mit_linkedin.csv")
people_df

# %%
