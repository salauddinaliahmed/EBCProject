from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
import requests
import pandas as pd
from selenium import webdriver
import csv
import pandas as pd
import os
from time import sleep

reviewer_name = []
reviwer_link = []
reviewer_level = []
reviewer_location = [] 
reviewer_contribution = []
reviewer_helpfulness = []
rev_each = []

def main():
    driver = webdriver.Chrome()
    #Collecting restaurant information
    restaurant_data = pd.read_csv('/Users/salauddinali/Desktop/Research Project EBC6997/test_reviews_old.csv', encoding="ISO-8859-1")

    #Collecting restaurant name and link.
    iterator_restaurant = restaurant_data[['Restaurant_name', 'Restaurant_link']]

    for r_name,r_link in iterator_restaurant.iterrows():
        url = r_link[1]
        driver.get(url)
        user_images = driver.find_elements_by_class_name('avatarWrapper')
        for each_image in user_images:
            driver.execute_script("arguments[0].click();", each_image)
            sleep(2)
            source = driver.page_source
            page = soup(source, "html.parser")
            stuff = page.find('div',{'class':'memberOverlayRedesign'})
            #print (stuff.find("h3", {"class":"username"}))
            #sleep(2)
            #driver.find_element_by_tag_name("body").click()


            reviewer_name.append(stuff.find('a').text)
            sleep(2)
            driver.find_element_by_tag_name("body").click()
        """
            reviewer_level.append(stuff.find('memberreviewbadge').text)
            reviewer_contribution.append(stuff.find('memberdescriptionReviewEnhancements').text)
            reviewer_contribution.append(stuff.find('badgeTextReviewEnhancements').text)
            reviewer_helpfulness.append(stuff.find('badgeTextReviewEnhancements').text)
            ratings_each = stuff.findAll('chartRowReviewEnhancements')
            for each_rating in ratings_each:
                rev_each.append(each_rating.text)

            sleep(5)
        sleep(15)
        """
 
if __name__ == '__main__':
    main()

