#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 14:18:39 2019

@author: salauddinali
"""
#importing Packages
import pandas as pd 
from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
import requests
import pandas as pd
from selenium import webdriver
import csv
import pandas as pd
import os
from time import sleep

#Initializing the browser
driver = webdriver.Chrome()

#importing the packages
complete_file = pd.read_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/rest_ds.csv', encoding = "ISO-8859-1")
links = list(set(complete_file["Rest_link"]))
del links[0:5]

# Initialiazing lists
restaurant_name =[]
reviewer_name = []
reviewer_link = []
reviewer_level = []
reviewer_location = []
reviewer_age = []
reviewer_contribution = [] #Reviewer contribution profile. 
safe = []
review_text = [] #list of reviews.
rev_each = [] #This is for the distribution of the rating
rev_rating = [] #each reviews rating
rating_date = [] #rating date
failed_links = []

for each_link in links:
    print (each_link)
    driver.get(each_link)
    driver.implicitly_wait(5)
    r_name = driver.find_element_by_tag_name('h1').text
    
    while True:
        try:    
            user_images = driver.find_elements_by_class_name('avatarWrapper')
            comment_check = driver.find_elements_by_class_name('prw_reviews_text_summary_hsx')
        except:
            break
        if len(user_images) ==  len(comment_check):
            for each_image in user_images:
                driver.execute_script("arguments[0].click();", each_image)
                sleep(0.7)
                user_tabs = driver.find_elements_by_class_name('memberOverlayRedesign')
                user_comments = driver.find_elements_by_class_name('prw_reviews_text_summary_hsx')
                
            for each_tab in user_tabs:
                
                #Exracting name
                try:
                    name = each_tab.find_element_by_class_name("username").text
                    reviewer_name.append(name)
                    restaurant_name.append(r_name)
                except:
                    reviewer_name.append('0')
                
                #Extraction of link
                try:
                    link = each_tab.find_element_by_tag_name("a")
                    reviewer_link.append("https://www.tripadvisor.ca/"+str(link.get_attribute('href')))
                except:
                    reviewer_link.append('0')
                
                #Extraction of user_level
                try: 
                    level = each_tab.find_element_by_class_name("badgeinfo").text
                    reviewer_level.append(level)
                except:
                    reviewer_level.append('0')
                
                #Extraction of reviewer_location
                try:
                    location_age = each_tab.find_element_by_class_name("memberdescriptionReviewEnhancements").text
                    reviewer_location.append(location_age)
                except:
                    pass
                
                #Extraction of Contributions
                try:
                    contributions = each_tab.find_elements_by_class_name('rowCellReviewEnhancements')
                    new_add = []
                    for each_contri in contributions:
                        new_add.append(each_contri.text)
                    reviewer_contribution.append(new_add)
                except:
                    reviewer_contribution.append('0')
                
                #Extraction of 
        else:
             driver.refresh
