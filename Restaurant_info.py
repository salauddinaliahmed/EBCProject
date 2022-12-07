from bs4 import BeautifulSoup as soup
from selenium.webdriver.common.by import By
import requests
import pandas as pd
from selenium import webdriver
import csv
import pandas as pd
import os
from time import sleep

#initializing web driver
driver = webdriver.Chrome()

#To Limit the search to ottawa.
URL = "https://www.tripadvisor.ca/Restaurants-g155004-Ottawa_Ontario.html"
PATH = "/Users/salauddinali/Desktop/"

#Creating lists to store data.
rest_name = []
rest_link = []
rest_rating = []
rest_ranking = [] # done
rest_pricing = [] #done
rest_offering = [] #done
rest_reviews = [] #done


# Singleton driver class.
# class BrowserDriver:
#     __instance = None

#     def __init__(self, driver):
#         if BrowserDriver.__instance != None:
#             return BrowserDriver.__instance
#         BrowserDriver.__instance = self
#         self.driver = driver

#     @property
#     def gdriver():
#         if BrowserDriver.__instance != None:
#             return BrowserDriver.__instance
#         else:
#             raise Exception(f"Singleton not initialized WebDriver{BrowserDriver.__instance}")


def goto_webpage(url):
    """Go to the url and click search."""
    driver.get(url)
    sleep(1)
    element = driver.find_element_by_id('secondaryText')
    driver.execute_script("arguments[0].click();", element)
    sleep(3)


#Saving restaurant name and restuarant link.
def do_scaping(base_url="https://www.tripadvisor.ca") -> dict:
    while True:
        sleep(1)
        #result = driver.find_elements_by_id('EATERY_SEARCH_RESULTS')
        b = driver.page_source
        page = soup(b, "html.parser")
        title = page.findAll('a',{"class": "property_title"})
        #rating = page.findAll('div', {"class": "rating"})
        #pricing = page.findAll('span', {"class": "item price"})
        each_block = page.findAll('div', {"class": "rebrand"})
        

        # Parsing through each block
        for each_entity in each_block:
            rating = each_entity.find('div',{"class":"rating rebrand"})
            reviews = each_entity.find('span', {"class":"reviewCount"})
            popularity = each_entity.find('div',{"class":"popIndexBlock"})
            pricing = each_entity.find('span',{"class":"item price"})
            speciality_text = each_entity.findAll('span',{"class":"item cuisine"})
            speciality_hyperlink = each_entity.findAll('a', {"class": "item cuisine"})
            title = each_entity.find('a', {"class": "property_title"})   
            
            #Adding Name
            if title == None:
                continue
            else:
                rest_name.append(title.text.strip('\n'))
                rest_link.append(base_url+ str(title.get('href')))

            #Adding rating.
            if rating == None:
                rest_rating.append('0')
            else:
                raw_rating = (rating.find('span'))
                value = raw_rating['class'][1]
                number = value.strip("bubble_")
                rest_rating.append(int(number)/10)

            #Adding reviews
            if reviews == None:
                rest_reviews.append('0')
            else:
                temp = reviews.text.strip('\n')
                temp = temp.strip(' reviews')
                rest_reviews.append(temp)
            
            #Adding popularity
            if popularity == None:
                rest_ranking.append('0')
            else:
                rest_ranking.append(popularity.text.replace('\n','').replace('#','').replace("of 2,269 Restaurants in Ottawa",''))
            
            #Adding Pricing
            if pricing == None:
                rest_pricing.append('0')
            else:
                rest_pricing.append(pricing.text)
        
            #Adding Speciality
            if speciality_text == None and speciality_hyperlink == None:
                rest_offering.append('0')
            else:
                dummy_list = []
                for each_speciality in speciality_text:
                    dummy_list.append(each_speciality.text)
                for each_hyperlink in speciality_hyperlink:
                    dummy_list.append(each_hyperlink.text)
                rest_offering.append(dummy_list)
        try:
            
            sleep(2)
            element = page.find('a',{"class":'next'})
            extension = element.get('href')
            url = base_url + extension
            driver.get(url) 
        except:
            break
        return {
        "Restaurant_name": rest_name, "Restaurant_link":rest_link, 
        "Restaurant_rating": rest_rating,"Restaurant_reviews": rest_reviews, 
        "Restaurant_offering:":rest_offering, "Restaurant_pricing": rest_pricing
        }

def print_data(data):
    """Get data size."""
    for k,v in data.items():
        print(f"Rows in {k} is {v}")

def save_data(path, data):
    """Save data on disk."""
    df_rest = pd.DataFrame(data)
    df_rest.to_csv('test_reviews.csv')


if __name__ == "__main__":
    goto_webpage(URL)
    result = do_scraping()
    print_data(result)
    save_data(PATH,result)
