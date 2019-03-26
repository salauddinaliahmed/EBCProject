# This program only collects reviewer data
import pandas as pd 
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
import requests
import pandas as pd
import selenium
import csv
import os
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities().FIREFOX
caps["pageLoadStrategy"] = "none"

name = []
followers = []
following = []
error_links = []
#Loading the data
user_data = pd.read_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/user_links.csv', encoding = "ISO-8859-1")
links = list(user_data['Reviewer_Link'])

driver=selenium.webdriver.Firefox(executable_path="/Users/salauddinali/Downloads/geckodriver")
driver.implicitly_wait(7)

for each_link in links:
    sleep(0.5)
    try:
        driver.get(each_link)
        sleep(1)
        name.append(driver.find_element_by_tag_name('h1').text)
        followers.append(driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/div[2]/span[2]').text)
        following.append(driver.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/div/div[1]/div/div/div/div[3]/span[2]').text)
    except:
        name.append('0')
        followers.append('0')
        following.append('0')
        error_links.append(each_link)

    followers_following = pd.DataFrame({'Name':name, 'Followers': followers, 'Following': following})
    followers_following.to_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/followers_following.csv')
error_link = pd.DataFrame({'error_link': error_links})
error_link.to_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/errors.csv')
            