'''this is the test file of naukri.com'''
import os
import time
import datetime
import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")

def naukri_job_scraper():
    # Set up Chrome options
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')

    # Initialize DataFrame
    dff = pd.DataFrame(columns=['Job Title','Description', 'Experience Reqd', 'Company', 'City', 'Salary Range', 'Date Posted', 'URL'])

    # Initialize WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    url = "https://www.naukri.com/python-jobs?k=python"
    driver.get(url)

    time.sleep(3)
    try: 
        driver.find_element(By.XPATH, '//*[@id="root"]/div[4]/div[1]/div/section[2]/div[1]/div[2]/span/span[2]/p').click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div[4]/div[1]/div/section[2]/div[1]/div[2]/span/span[2]/ul/li[2]').click()
    except Exception as e:
        pass

    pages = np.arange(1,11)

    # Define directory path
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    # Create directory if it doesn't exist
    create_directory_if_not_exists(directory_path)

    for page in pages:
        soup = BeautifulSoup(driver.page_source,'html5lib')
        results = soup.find(id='listContainer')

        try:
            job_elems = results.find_all('div', class_='srp-jobtuple-wrapper')
        except Exception as e:
            print("Internet connect is not stable, run the program again")

        for job_elem in job_elems:
            T = job_elem.find('a',class_='title')
            Title = T.text

            try:
                D = job_elem.find('span', class_='job-desc')
                Description = D.text
            except Exception as e:
                Description = None

            E = job_elem.find('span', class_='expwdth')
            if E is None:
                Exp = "Not-Mentioned"
            else:
                Exp = E.text

            C = job_elem.find('a', class_='comp-name')
            Company = C.text

            try:
                C = job_elem.find('span', class_='locWdth')
                City = C.text
            except Exception as e:
                City = None

            try:
                S = job_elem.find('span', 'ni-job-tuple-icon ni-job-tuple-icon-srp-rupee sal')
                Salary = S.text
                print("Salary: ", Salary)
            except Exception as e:
                Salary = "Not-Mentioned"
                print("Salary Not Found")

            D = job_elem.find('span', class_='job-post-day')
            try: 
                if D == 'Just Now':
                    Date = 'Today'
                else:
                    Date = D.text
            except Exception as e:
                Date = None

            U = job_elem.find('a',class_='title').get('href')
            URL = U

            dff = pd.concat([dff, pd.DataFrame([[Title, Description, Exp, Company, City, Salary, Date, URL]], columns=['Job Title','Description', 'Experience Reqd', 'Company', 'City', 'Salary Range', 'Date Posted', 'URL'])], ignore_index=True)
            print(dff)

            dff.to_excel(os.path.join(directory_path, "NaukriJobListing_" + str(datetime.date.today()) + ".xlsx"), index=False)

        driver.execute_script("window.scrollTo(0,(document.body.scrollHeight) - 1500)")

        time.sleep(0.75)

        driver.find_element(By.XPATH, '//*[@id="lastCompMark"]/a[2]/span')

        time.sleep(3)

    print("*********************CONCLUSION: FINISHED FETCHING DATA FROM NAUKRI.COM*********************")

    driver.close()

# naukri_job_scraper()
