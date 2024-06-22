from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from bs4 import BeautifulSoup
import time
import pandas as pd
import datetime
import os
import numpy as np

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")

def job_data_scraper(job_role, ai_url, page):
    #service = Service(executable_path=r'C:\Programming\Project\New folder\web-scraping-naukri-main\web-scraping-naukri-main\chromedriver.exe')
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    
    df = pd.DataFrame(columns=["Title", "Company", "Job Type", "Salary", "Experience", "City", "URL"])

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    url = ai_url

    driver.get(url)

    soup = BeautifulSoup(driver.page_source, 'html5lib')

    page_count = page

    try:

        if page_count is not None:
            click = int(page_count)
    
    except  Exception as e:

        # soup = BeautifulSoup(driver.page_source, 'html5lib')
        total = soup.find('em', id="job-search-count").text
        count = total.split(" ")
        c = int(count[0])
        if c >= 50:
            click = c // 50
        else:
            click = 1
    directory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Ai_jobs')
    create_directory_if_not_exists(directory_path)

    pages = np.arange(0, click)
    for page in pages:
        results = soup.find('ul', class_='list-group list-group-flush mb-4')
        time.sleep(10)
        job_elems = results.find_all('li', class_='list-group-item list-group-item-action p-1')
        # print(len(job_elems))

        for job_elem in job_elems:
            title = job_elem.find('h2', class_="h5 mb-2 text-body-emphasis")
            Title = title.text

            comp_name = job_elem.find('p', class_='m-0 text-muted')
            Company = comp_name.text

            job_type = job_elem.find('span', class_='badge rounded-pill text-bg-secondary my-md-1 ms-1')
            Job = job_type.text

            sal = job_elem.find('span', class_='badge rounded-pill text-bg-success d-none d-md-inline-block')
            if sal is None:
                Salary = "Not-Mentioned"
            else:
                Salary = sal.text

            try:
                exp = job_elem.find('span', class_='badge rounded-pill text-bg-info my-md-1 d-md-none')
                Experience = exp.text
            except Exception as e:
                print('Experience : Not-mentioned')
                Experience = "Not-Mentioned"

            loc = job_elem.find('span', class_='d-block d-md-none text-break')
            City = loc.text

            U = job_elem.find('a', class_='col pt-2 pb-3').get('href')
            URL = f'URL : "https://ai-jobs.net{U}'

            df = pd.concat([df, pd.DataFrame([[Title, Company, Job, Salary, Experience, City, URL]],
                                             columns=['Title', 'Company', 'Job Type', 'Salary', 'Experience', 'City',
                                                      'URL'])], ignore_index=True)
            print(df)
            df.to_excel(os.path.join(directory_path, f"{job_role}_Ai_JobListing_" + str(datetime.date.today()) + ".xlsx"), index=False)

    time.sleep(0.75)
    load_jobs = driver.find_element(By.CSS_SELECTOR, ".list-group-item.list-group-item-action.text-center.pt-3")
    driver.execute_script("arguments[0].scrollIntoView();", load_jobs)

    action = ActionChains(driver)

    action.double_click(on_element=load_jobs)

    action.perform()

    time.sleep(3)

    print("*********************CONCLUSION: FINISHED FETCHING DATA FROM ai-jobs.net*********************")

    driver.close()

# job_data_scraper()
