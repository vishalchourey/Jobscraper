'''This program is used for creating a custome link according to user input '''

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService



def custom_url(job_role, experience, location):

    # service = Service(
    #     executable_path=r'C:\Programming\Project\New folder\web-scraping-naukri-main\web-scraping-naukri-main\chromedriver.exe')
    # chrome_options = Options()

    # chrome_option.add_argument
    # Set up Chrome options
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    # Initialize WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    url = "https://www.naukri.com/"
    # https://www.naukri.com/java-jobs-in-hyderabad-secunderabad?k=java&l=hyderabad
    # https://www.naukri.com/java-jobs-in-hyderabad-secunderabad?k=java&l=hyderabad&experience=1
    # https://www.naukri.com/java-jobs?k=java&experience=1
    # https://www.naukri.com/java-jobs?k=java
    driver.get(url)

    time.sleep(3)

    if job_role is not None:
        # search_Bar
        try:
            # Search_Bar
            Search_bar = driver.find_element(By.XPATH,
                                             "//input[contains(@placeholder,'Enter skills / designations / companies')]")
            Search_bar.click()
            Search_bar.send_keys(job_role)

        except Exception as e:
            print("No record found!")

            # Location
        if location is not None:

            # Location
            try:
                job_loc = driver.find_element(By.XPATH, "//input[@placeholder='Enter location']")
                job_loc.click()
                job_loc.send_keys(location)
            except Exception as e:
                pass

            # Search_Button
            try:
                Search_Button = driver.find_element(By.XPATH, "//div[@class='qsbSubmit']").click()
            except Exception as e:
                pass
            if experience is not None:
                new_url = driver.current_url + f"&experience={int(experience)}"

                return new_url



    driver.close()

# job = input("enter job role:")
# exp = input("enter experience")
# loc = input(("enter location: "))

# URL = custom_url(job, exp, loc)
# print(URL)