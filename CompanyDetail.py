from queue import Queue
import threading
from selenium.webdriver.chrome.options import Options
import selenium.webdriver as uc
from selenium.webdriver.common.by import By
import cookie
from datetime import datetime as time
import time as tm
import url as u
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

DRIVER_PATH = "venv/Media/chromedriver"
COOKIE_PATH = "venv/Media/Cookie.txt"
COMPANY_PATH = input("Enter Path: ")
FILE_PATH = "venv/Media/Datail_"+ (COMPANY_PATH[len("venv/Media/"):])
LOG_PATH = "venv/Media/DatailLog_"+ (COMPANY_PATH[len("venv/Media/"):])

def optionsSetter(urlOrg = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=0&page=1&industry=" + str(200132) + "&filterType=RATING_OVERALL"):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("window-size=1280,800")
    #ua = UserAgent(browsers='chrome', os='macos')
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    #ua.random
    #driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent}) 
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.images": 2})
    driver = uc.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.delete_all_cookies()
    driver.get(urlOrg)
    cookie.load_cookie(driver, COOKIE_PATH)
    driver.refresh()
    return driver

try:
    open(LOG_PATH, "x")
    open(FILE_PATH, "x")
except:
    print("File was generated before!")
    
# Öffne die TXT-Datei im Lesemodus
def scraper(driver: uc.Chrome, lines):
    global readedLines  # Declare that you want to modify the global variable
    for line in lines:
        try:
            # Wait for the page to load completely
            wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
            companyDetail = []
            # Verwende eval(), um den Text in ein Python-Datenobjekt umzuwandeln (in diesem Fall ein Dictionary)
            data = eval(line)
            # Drucke die reviewUrl aus dem Dictionary
            urlData = u.urlParse(data['reviewUrl'])
            url = u.urlCreate(
            companyId=urlData["companyId"],
            companyName=urlData["companyName"],
            urlType="CompanyDetail",
            )
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-test="companyDetails"]')))
            if not (driver.find_elements(By.CSS_SELECTOR, '[data-test="companyDetails"]')):  raise ValueError('Help Protect Glassdoor!') 
            
            companyDetailsElement = driver.find_element(By.CSS_SELECTOR, '[data-test="companyDetails"]')
            liTags = companyDetailsElement.find_elements(By.TAG_NAME,'li') 
            
            companyDetail.append(urlData["companyId"])
            companyDetail.append(urlData["companyName"])
            
            for li in liTags:
                companyDetail.append(li.text)
            
            
            with open(FILE_PATH, "a") as f:
                    f.write(f"{companyDetail}\n")
            
            with open(LOG_PATH, "a") as f:
                f.write(
                    str(time.now())
                    +"       OK  "
                    + str(readedLines + 1) 
                    + "/" 
                    + str(len(lines))
                    + f"\n")
            readedLines = readedLines + 1
        except TimeoutException:
            with open(LOG_PATH, "a") as f:
                f.write(
                    str(time.now())
                    +"   NOT OK  "
                    + str(readedLines + 1) 
                    + "/" 
                    + str(len(lines))
                    + "Detected"
                    + f"\n")
            driver.quit()
            break
        except ValueError as error:
            with open(LOG_PATH, "a") as f:
                f.write(
                    str(time.now())
                    +"   NOT OK  "
                    + str(readedLines + 1) 
                    + "/" 
                    + str(len(lines))
                    + f"\n")
            driver.quit()
            break


with open(COMPANY_PATH, 'r') as file:
    lines = file.readlines()

readedLines = 0
while (len(lines) > 0):
    if readedLines != 0:
        tm.sleep(20)

    driver= optionsSetter()
    
    readedLines = 0
    scraper(driver,lines)
    
    with open(COMPANY_PATH, 'w') as file:
        file.writelines(lines[readedLines:])
    
    with open(COMPANY_PATH, 'r') as file:
        lines = file.readlines()

driver.quit()