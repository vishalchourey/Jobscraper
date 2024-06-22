from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

import os
import pandas as pd
import numpy as np 
import time 
import datetime

CHROMEDRIVER_PATH = r'C:\Programming\Project\New folder\web-scraping-naukri-main\web-scraping-naukri-main\chromedriver.exe'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()

# chrome_options.add_argument("--headless")
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')

service = Service(CHROMEDRIVER_PATH)

def timesjob_scraper():

    dff = pd.DataFrame(columns = ['Job Title', 'Description', 'Experience Reqd', 'Company', 'City', 'Salary Range', 'Date Posted', 'URL'])
    
    driver = webdriver.Chrome(service = service, options = chrome_options)

    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=&txtLocation=India#'
    driver.get(url)

    # print(driver.page_source) 
    
    time.sleep(10)

    try:
       driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/table/tbody/tr/td[2]/div/span').click()
    except Exception as e:
        print('EXCEPTION OCCURED')
        pass
    
    page_counter = 0
    
    # print(result2)
    pages = np.arange(1, 10)

    exception = 0

    for pages in pages:

        if page_counter == 0:
            next_counter = 0 
        else:
            next_counter = 1
        
        page_next_counter = np.arange(2,12)

        for page_next in page_next_counter:
    
            try:
                driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/table/tbody/tr/td[2]/div/span').click()
            except Exception as e:
                print('EXCEPTION OCCURED \n  x not present in the screen \n')
                pass        

            soup = BeautifulSoup(driver.page_source, 'html5lib')
            
            # print(soup.encode('utf-8'))

            try:
                    driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/table/tbody/tr/td[2]/div/span').click()
            except Exception as e:
                print('EXCEPTION OCCURED \n  x not present in the screen \n')
                pass
            try:
                driver.find_element(By.XPATH, '//*[@id="closeSpanId"]').click()
            except Exception as e:
                print('EXCEPTION OCCURED \n  x ver 2 not present in the screen \n')
                pass

            result = soup.find('ul', class_='new-joblist')
            result2 = result.find_all('li', class_='clearfix job-bx wht-shd-bx')
            
            for i in result2:
                
                # TITLE
                title = i.find('a')
                title = title.text.strip()
                # print(title.encode('utf-8'))
                
                # Description
                description = i.find('label').next_sibling.strip()
                # print(description)

                # COMPANY
                text = i.find('h3', class_='joblist-comp-name')
                text = text.text
                initial_company = text.find('(')
                Company = text[:initial_company]
                Company = Company.strip()   
                # print(Company)

                # Exp
                Mat_icons = i.find_all('i', class_='material-icons')
                # print('THIS IS MATERIAL ICONS:', Mat_icons)
                Exp = Mat_icons[0].next_sibling.text.strip()
                # print(Exp)

                # City
                spans = i.find_all('span')
                City = spans[1].text

                # Date Posted
                Date = i.find('span', class_='sim-posted')
                Date = Date.text.strip()
                # print(Date)

                URL = i.find('a').get('href')
                # print(URL)

                try:
                    Salary = i.find('i', class_="material-icons rupee").next_sibling
                    # print(Salary)
                except Exception as e:
                    print("EXCEPTION OCCURRED AT SALARY")
                    exception = exception + 1
                    Salary = 'Not Mentioned'
                
                dff = pd.concat([dff, pd.DataFrame([[title, description , Exp, Company, City, Salary, Date, URL]], columns = ['Job Title','Description', 'Experience Reqd', 'Company', 'City', 'Salary Range', 'Date Posted', 'URL'])], ignore_index=True)
                
            print(dff)

            dff.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', "TimesJobs_" + str(datetime.date.today()) + ".xlsx"), index=False)
            
            driver.execute_script("window.scrollTo(0,(document.body.scrollHeight))")
            
            scroll_time = 2
            time.sleep(scroll_time)
            
            dff.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', "TimesJobs_" + str(datetime.date.today()) + ".xlsx"), index=False)
            
            page_counter = page_counter + 1

            final_page_next = next_counter + page_next
            try: 
                driver.find_element(By.XPATH, '/html/body/div[3]/div[4]/section/div[2]/div[2]/div[4]/em[' + str(final_page_next) + ']/a').click()
            except Exception as e:
                print('EXCEPTION OCCURED (UNABLE TO FIND THE BUTTON)\n', e, '\n********** KINDLY LOOK AFTER IT **********')

            loading_time = 1
            time.sleep(loading_time)

            print('NUMBER OF EXCEPTIONS: ', exception)

