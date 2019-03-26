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


#caps = DesiredCapabilities().FIREFOX
#caps["pageLoadStrategy"] = "none"

name = []
followers = []
following = []
error_links = []
#Loading the data
user_data = pd.read_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/user_links.csv', encoding = "ISO-8859-1")
links = list(user_data['Reviewer_Link'])

for each_link in links:
    sleep(1)
    r = requests.get(each_link)
    page = soup(r.content,"html.parser")
    try:
        sleep(1)
        n = page.find('h1').text
        if n==None:
            name.append('0')
        else:    
            name.append(n)
        data_f = page.findAll('span', {'class':'social-member-MemberStats__stat_item_count--14i7c'})
        if data_f == None:
            followers.append('0')
            following.append('0')
        elif data_f[1]==None:    
            followers.append('0')
        elif data_f[1]==None:
            following.append('0')
        else:
            followers.append(data_f[1].text) 
            following.append(data_f[2].text)
    except:
        error_links.append(each_link)

    followers_following = pd.DataFrame({'Name':name, 'Followers': followers, 'Following': following})
    followers_following.to_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/followers_following.csv')
error_link = pd.DataFrame({'error_link': error_links})
error_link.to_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/errors.csv')
            