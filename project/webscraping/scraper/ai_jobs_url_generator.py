"""This the program to generate cumstome url"""
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service  # it use for working with chrome webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


# service = Service(executable_path= r'C:\Programming\Project\New folder\web-scraping-naukri-main\web-scraping-naukri-main\chromedriver.exe' )
# chrome_options = Options()

# chrome_option.add_argument
# Set up Chrome options
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
    
# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    


def url_generator(job_role):
    
    url = "https://ai-jobs.net/"

    driver.get(url)

    time.sleep(3)
    
    #search_Bar
    try:
        # job_role 
        Search_bar = driver.find_element(By.XPATH, "//input[@id='id_key']")
        Search_bar.click()
        Search_bar.send_keys(job_role)

    except Exception as e:
        print ("No record found!")

        pass

    # #Location
    # try:
    #     #country
    #     job_loc = driver.find_element(By.XPATH, "//input[@placeholder='Countries 🛂']")
    #     job_loc.click()
    #     job_loc.send_keys("India")
    #     job_loc.send_keys(Keys.RETURN)
    # except Exception as e:
    #     pass
    #
    # time.sleep(5)
    #
    # try:
    #     #city
    #     job_city = driver.find_element(By.XPATH, "//input[@placeholder='Cities 🏢']")
    #     job_city.click()
    #     job_city.send_keys(city)
    # except Exception as e:
    #     pass
    # time.sleep(5)
    #search_Button
    try:
        
        job_city = driver.find_element(By.XPATH, "//button[normalize-space()='Search']")
        job_city.click()
        return driver.current_url
    
    except Exception as e:
        pass

    time.sleep(5)

    



    driver.close()





