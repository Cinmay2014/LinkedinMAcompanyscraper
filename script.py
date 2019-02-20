#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pymongo
import parameters
from bs4 import BeautifulSoup
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import NoSuchElementException
# headless browser
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

# browser to monitor how it works
# driver = webdriver.Chrome()



# define database
client = pymongo.MongoClient('localhost', 27017)
db = client['lknew1']  # name db
collection = db['lkcomp1']  # name collection


# use selenium to login
def login():
    driver.get('https://www.linkedin.com')
    username = driver.find_element_by_class_name('login-email')
    username.send_keys(parameters.linkedin_username)
    sleep(0.5)
    password = driver.find_element_by_class_name('login-password')
    password.send_keys(parameters.linkedin_password)
    sleep(0.5)
    sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
    sign_in_button.click()
    sleep(2)

# create website address
# read company name from txt file
f = open('C:/Users/yidon/Desktop/MA1.txt','r')
x = f.readlines()
url = 'https://www.linkedin.com/company/'
# use lambda function to create url lists
linkedin_urls = [url+i.strip()+'/' +'about' for i in x]


# get information
def comp_info(linkedin_urls):

    for linkedin_url in linkedin_urls:
        # sleep(1.5)
        try:
            sleep(1.5)
            driver.get(linkedin_url)
            soup = BeautifulSoup(driver.page_source, 'lxml')

            try:
                if len([soup.select('dl')])>=1:
                    overview = [soup.select('dl')[0]]
                    file = open('success.txt', 'a', encoding='utf-8')
                    file.write(linkedin_url + '\n')
                    file.close()
                else:
                    pass
            except:

                pass

            # sleep(1.5)
            try:
                for i in overview:
                    # find company information
                    keys = []
                    for key in i.select('dt'):
                        key = key.text.strip()
                        keys.append(key)
                    # find values
                    values = []
                    for value in i.select('dd'):
                        value = value.text.strip()
                        values.append(value)
                    # use zip to create dict
                    comp_info = dict(zip(keys, values))
                    # return comp_info
                    name = soup.h1.get_text().strip()
                    comp_info.update({'name':name})
                    # print(comp_info)
                # insert to mongodb
                result = collection.insert_one(comp_info)
                print(result)
            except:
                pass

        except:
            pass
        continue

def main():
    login()
    comp_info(linkedin_urls)

# main function
main()

# quit browser
driver.quit()