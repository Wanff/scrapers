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

#%%
def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

# %%
driver = uc.Chrome(headless=False,use_subprocess=True)
driver.implicitly_wait(10)

query = "Stanford"

driver.get('https://www.ycombinator.com/companies?query='+query)

time.sleep(3 + 2*np.random.rand())
scroll_down(driver)
time.sleep(5 + 2*np.random.rand())

companies_tags = driver.find_elements(By.CLASS_NAME, "_company_lx3q7_339")

# wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "_company_lx3q7_339")))

time.sleep(np.random.rand())
company_links = [company.get_attribute("href") for company in companies_tags]
print(len(company_links))

companies = []

for link in company_links:
    print(link)
    driver.get(link)
    
    time.sleep(np.random.rand())
    # company_name_h1 = driver.find_element(By.TAG_NAME, "h1")
    # company_name = company_name_h1.find_element(By.TAG_NAME, "h1").text
    company_name = driver.find_element(By.TAG_NAME, "h1").text
    text_descs = driver.find_elements(By.CLASS_NAME, "whitespace-pre-line")
    
    yc_meta_tags = driver.find_elements(By.CLASS_NAME, "yc-tw-Pill")
    yc_meta = [tag.text for tag in yc_meta_tags]
    
    company_desc = text_descs[0].text
    
    founder_bios = [text_descs[i].text for i in range(1, len(text_descs))]
    
    founder_divs = driver.find_elements(By.CLASS_NAME, "leading-snug")
    
    if len(founder_bios) != len(founder_divs):
        founder_bios = [None for _ in range(len(founder_divs))]
        
    founders = []
    for i, founder in enumerate(founder_divs):
        founder_name = founder.find_elements(By.TAG_NAME, "div")[0].text
        founder_linkedin = None
        founder_twitter = None
        
        link_div = founder.find_elements(By.TAG_NAME, "div")[1]
        for a_tag in link_div.find_elements(By.TAG_NAME, "a"):
            if "linkedin" in a_tag.get_attribute("href"):
                founder_linkedin = a_tag.get_attribute("href")
            elif "twitter" in a_tag.get_attribute("href"):
                founder_twitter = a_tag.get_attribute("href")
        
        founders.append({
            "name": founder_name,
            "linkedin": founder_linkedin,
            "twitter": founder_twitter,
            "bio": founder_bios[i],
        })
        print(company_name, yc_meta, founder_name, founder_linkedin, founder_twitter)
    
    companies.append({"company_name": company_name, 
                      "desc": company_desc,
                      "yc_meta": yc_meta,
                      "yc_link": link,
                      "founders": founders
                    })
        
    time.sleep(np.random.rand() / 10)

driver.quit()

# %%
pickle.dump(companies, open("stanford_yc_companies.pickle", "wb"))
# %%
companies
# %%
#* postprocess yc scrapes
# Load the pickle file
harvard_yc_companies = pickle.load(open("harvard_yc_companies.pickle", "rb"))
mit_yc_companies = pickle.load(open("mit_yc_companies.pickle", "rb"))
stanford_yc_companies = pickle.load(open("stanford_yc_companies.pickle", "rb"))

all_yc_companies = harvard_yc_companies + mit_yc_companies + stanford_yc_companies
schools = ["Harvard"] * len(harvard_yc_companies) + ["MIT"] * len(mit_yc_companies) + ["Stanford"] * len(stanford_yc_companies)

founders = []
for i, company in enumerate(companies):
    if "ACTIVE" in company['yc_meta']:
        for founder in company['founders']:
            if founder['bio'] is not None:
                # if "Harvard" in founder['bio'] or "MIT" in founder['bio'] or "Stanford" in founder['bio']:
                    founders.append({
                        "company_name": company['company_name'],
                        "founder_name": founder['name'],
                        "founder_linkedin": founder['linkedin'],
                        "founder_twitter": founder['twitter'],
                        "founder_bio": founder['bio'],
                        "yc_link": company['yc_link'],
                        "school": schools[i]
                    })

len(founders)


# %%
pickle.dump(founders, open("yc_founders.pickle", "wb"))
# %%
