#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 09:06:59 2019

@author: salauddinali
"""
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
import requests
import pandas as pd
from selenium import webdriver
import csv
import pandas as pd
import os
from time import sleep


 #Iterating through rows of the DataFrame
df_reviews = pd.DataFrame(columns = ["Restaurant", "Reviewer", "Location", "Review"])

df_rest = pd.read_csv('/Users/salauddinali/Desktop/Restaurants_Links.csv')
driver = webdriver.Chrome('/Users/salauddinali/Downloads/chromedriver')
for r_count,r_link in df_rest.iterrows():
    url = r_link[2]     
    while True:
        #clicking on more to get the entire text. One click per page should be fine.
        try:
            
            driver.get(url)
            element = driver.find_element_by_class_name('ulBlueLinks')
            driver.execute_script("arguments[0].click();", element)
            
        except:
            pass
        sleep(1)
        #pop = driver.current_url
        b = driver.page_source
        page = soup(b, "html.parser")
        #Saving reviews from on page in a list 
        try:
            review_blob = page.findAll('div', {"class": "prw_reviews_review_resp"})
            for each_blob in review_blob:
                rest_name = r_link[1]
                temp = each_blob.find('div',{"class":"info_text"})
                rev_name = temp.find('div', {"class":""}).text
                try:
                    rev_loc = each_blob.find('div', {"class":"userLoc"}).text
                except:
                    rev_loc = None
                review_text = each_blob.find('p').text
                #Apparently dataframes are not so good for appending data according to Sentdex(Youtube). But, i am using it anyways
                df_reviews = df_reviews.append({'Restaurant': rest_name, 'Reviewer': rev_name, 'Location' : rev_loc, 'Review' : review_text}, ignore_index=True)
                sleep(1)
            try:
                sleep(2)
                element = page.find('a',{"class":'next'})
                extension = element.get('href')
                url = "https://www.tripadvisor.ca"+extension

            except:
                break 
        except:
            pass

df_reviews.to_csv("/Users/salauddinali/Desktop/Restaurants_Reviews.csv")


    
