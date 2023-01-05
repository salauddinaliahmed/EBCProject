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



#Loading the data
complete_file = pd.read_csv('/Users/salauddinali/Desktop/incomplete.csv', encoding = "ISO-8859-1")
links = list(set(complete_file["Restaurant_link"]))
print (links)
done_links = []


#Storage containers
restaurant_name =[]
reviewer_name = []
reviewer_link = []
reviewer_level = []
reviewer_location = []
reviewer_age = []
reviewer_contribution = []
rev_each = [] #This is for the distribution of the rating
safe = []

#DataFrame
def main():

    driver=selenium.webdriver.Firefox(executable_path="/Users/salauddinali/Downloads/geckodriver")
    driver.implicitly_wait(5)
    for each_link in links:
        try:
            driver.get(each_link)
            r_name = driver.find_element_by_tag_name('h1').text
            while True:
                driver.implicitly_wait(5)
                user_images = driver.find_elements_by_class_name('avatarWrapper')
                for each_image in user_images:
                    driver.execute_script("arguments[0].click();", each_image)
                    sleep(0.5)
                source = driver.page_source
                page = soup(source, "html.parser")
                stuff = page.findAll('div',{'class':'memberOverlayRedesign'})
                if len(stuff) == 0:
                    restaurant_name.append(r_name)
                    reviewer_name.append('0')
                    reviewer_link.append('0')
                    reviewer_level.append('0')
                    reviewer_age.append('0')             
                    reviewer_location.append('0')
                    reviewer_contribution.append('0')
                    rev_each.append('0')
                else:
                    pass

                for each_f in stuff:
                    #print (stuff.find("h3", {"class":"username"}))
                    #driver.find_element_by_tag_name("body").click()
                    restaurant_name.append(r_name)
                    driver.implicitly_wait(20)
                    rev_name = each_f.find('a')
                    if rev_name == None:
                        reviewer_name.append('0')
                        reviewer_link.append('0')
                    else:
                        reviewer_name.append(rev_name.text.strip('\n'))
                        reviewer_link.append("https://www.tripadvisor.ca"+ str(rev_name.get('href')))

                    rev_level = each_f.find('div',{'class':'memberreviewbadge'})
                    if rev_level == None:
                        reviewer_level.append('0')
                    else:
                        reviewer_level.append(rev_level.text.strip('\n'))

                    rev_loc_join = each_f.find('ul', {'class': 'memberdescriptionReviewEnhancements'})
                    if rev_loc_join == None:
                        reviewer_age.append('0')             
                        reviewer_location.append('0')

                    else:
                        blob = rev_loc_join.text.lstrip('\n').rstrip('\n').split('\n')
                        safe.append(blob)
                        if len(blob) == 2:
                            reviewer_age.append(blob[0])
                            reviewer_location.append(blob[1])
                        else:
                            reviewer_age.append(blob[0])
                            reviewer_location.append('0')


                    rev_data = each_f.findAll('li',{'class':'countsReviewEnhancementsItem'})
                    if rev_data == None:
                        reviewer_contribution.append('0')
                    else:
                        new_list = []
                        for each_text in rev_data:
                            new_list.append(each_text.text.strip('\n'))
                        reviewer_contribution.append(new_list)

                    rating_each = each_f.findAll('span',{'class':'rowCountReviewEnhancements'})
                    if rating_each == None:
                        rev_each.append('0')
                    else:
                        brand_new = []
                        for each_rating in rating_each:
                            brand_new.append(each_rating.text)
                        rev_each.append(brand_new)

                    b = driver.page_source
                    page = soup(b, "html.parser")
                try:
                    sleep(1)
                    element = page.find('a',{"class":'next'})
                    extension = element.get('href')
                    url = "https://www.tripadvisor.ca"+ extension
                    driver.get(url) 
                except:
                    break
                sleep(0.3)
                Reviwer_data = pd.DataFrame({'Restaurant_name':restaurant_name, 'Reviwer_Name': reviewer_name, 'Reviewer_Link': reviewer_link, 'Reviewer_Level': reviewer_level, 'Reviewer_Age': reviewer_age, 'Reviwer_Location': reviewer_location, 'Reviewer_Contribution': reviewer_contribution, 'Reviewer_distribution': rev_each})
                Reviwer_data.to_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/reviewer_data.csv')
                done_links.append(each_link)
                sleep(0.3)
        except:
            pd.DataFrame({'Restaurant_link': done_links}).to_csv('/Users/salauddinali/Desktop/Research Project EBC6997/Dataset/done_links.csv')
            
        
if __name__ == "__main__":
    main()
