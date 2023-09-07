from queue import Queue
import threading
from selenium.webdriver.chrome.options import Options
import selenium.webdriver as uc
from selenium.webdriver.common.by import By
import cookie
from datetime import datetime as time
import time as tm
import url as u

DRIVER_PATH = "venv/Media/chromedriver"
COOKIE_PATH = "venv/Media/Cookie.txt"
companypath = input("Enter Path")
FILE_PATH =  "venv/Media/GenerateFile.txt"
LOG_PATH = "LOG_" + companypath
def optionsSetter(urlOrg = "https://www.glassdoor.com"):
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
    driver = uc.Chrome(options=options)
    driver.delete_all_cookies()
    driver.get(urlOrg)
    cookie.load_cookie(driver, COOKIE_PATH)
    driver.refresh()
    return driver

try:
    open(FILE_PATH, "x")
except:
    print("File was generated before!")
    
# Öffne die TXT-Datei im Lesemodus
def scraper(driver: uc.Chrome):
    companyDeteils = []
    with open(companypath, 'r') as file:
        # Iteriere über jede Zeile in der Datei
        for line in file:
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
            companyDetailsElement = driver.find_element(By.CSS_SELECTOR, '[data-test="companyDetails"]')
            liTags = companyDetailsElement.find_elements(By.TAG_NAME,'li') 
            for li in liTags:
                # Hier kannst du Aktionen für jedes li-Element durchführen
                # Zum Beispiel kannst du den Text des li-Elements ausgeben:
                companyDetail.append(li.text)
            companyDeteils.append(companyDetail)
            
            with open(FILE_PATH, "a") as f:
                for company in companyDeteils:
                    f.write(f"{company}\n") 

while (1>0):
    tm.sleep(20)
    driver= optionsSetter()
    scraper(driver)
