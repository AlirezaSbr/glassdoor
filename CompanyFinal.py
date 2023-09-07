import selenium.webdriver as uc
#import undetected_chromedriver as uc
from datetime import datetime as time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import xlsxwriter
import threading
from queue import Queue
import cookie
import queue
import time
from fake_useragent import UserAgent
import random


# Array containing [industrycode, pagenumber]
industry_page_array = [
    [200001,677],[200002,637],[200003,275],[200004,26],[200005,7],[200006,83],[200007,42],[200008,114],[200009,23],[200011,68],[200012,82],[200013,72],[200016,359],[200017,46],[200018,694],[200020,16],[200021,495],[200022,2039],[200023,722],[200024,385],[200025,75],[200027,165],[200028,1227],[200029,263],[200030,261],[200031,282],[200032,719],[200033,553],[200034,155],[200035,202],[200036,1944],[200037,345],[200038,70],[200039,78],[200040,496],[200041,36],[200042,53],[200043,142],[200044,702],[200045,529],[200046,1076],[200047,576],[200048,746],[200052,174],[200055,13],[200056,310],[200057,957],[200058,406],[200059,3643],[200060,1265],[200061,1007],[200063,605],[200064,1664],[200065,295],[200066,269],[200068,242],[200070,587],[200071,537],[200072,270],[200073,1248],[200074,294],[200075,260],[200076,101],[200077,213],[200080,346],[200082,297],[200083,80],[200085,86],[200087,158],[200088,255],[200089,1370],[200091,761],[200094,954],[200096,158],[200097,62],[200099,1611],[200100,24],[200101,115],[200102,136],[200103,122],[200105,567],[200106,85],[200107,200],[200109,49],[200110,67],[200111,253],[200113,39],[200115,319],[200116,34],[200117,101],[200118,29],[200119,651],[200120,174],[200122,259],[200127,25],[200128,24],[200130,502],[200132,27],[200134,89],[200135,501],[200139,474],[200144,120],[200145,100],[200146,817],[200147,1079],[200148,10],[200149,26],[200150,65],[200151,90],[200152,41],[200153,349],[200154,187],[200155,284],[200156,129],[200157,41],[200158,42],[200159,32],[200160,9],[200161,9],[200162,21],[200163,36],[200164,29],[200165,18],[200166,17]
]

# Paths
DRIVER_PATH = "venv/Media/chromedriver"
COOKIE_PATH = "venv/Media/Cookie.txt"
LOG_PATH = "venv/Media/Log.txt"
EXCEL_PATH = "venv/Media/companies.xls"
COMPANIES_FILE = "venv/Media/companies.txt"
NUM_THREADS = 4  # Adjust the number of threads as needed

# Selenium options
options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window-size=1280,800")
# options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

################################

# url = "www.glassdoor.de/Reviews/index.htm?overall_rating_low=0&page={}&industry={}&filterType=RATING_OVERALL".format(1, 2000001)
# driver = uc.Chrome(options=options, executable_path=DRIVER_PATH)
# driver.get(url)
# cookie.save_cookie(driver,COOKIE_PATH)
################################

# Function to perform scraping for a specific industry-page combination
def scrape_industry_page(industry_number, page_max):
    url = "https://www.glassdoor.de/Reviews/index.htm?overall_rating_low=0&page={}&industry={}&filterType=RATING_OVERALL".format(1, industry_number)
    ua = UserAgent(browsers='chrome', os='macos')
    user_agent = ua.random
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": user_agent}) 
    #options.add_argument(f'--user-agent={user_agent}')
    driver = uc.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get(url)
    driver.delete_all_cookies()
    cookie.load_cookie(driver, COOKIE_PATH)
    driver.refresh()
    for pagenumber in range(1, page_max + 1):
        try:
            companies = []
            url = "https://www.glassdoor.de/Reviews/index.htm?overall_rating_low=0&page={}&industry={}&filterType=RATING_OVERALL".format(pagenumber, industry_number)
            driver.get(url)
            # scraping logic 
                # Find all <a> tags with the specified attribute
            time.sleep(random.randrange(0,2)%random.randint(1,5))
            a_tags_with_data_test = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="cell-Reviews-url"]')
                # Handle No results
            if (len(a_tags_with_data_test) > 0): 
                time.sleep(3.332)
                driver.refresh()
                a_tags_with_data_test = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="cell-Reviews-url"]')
            if (len(a_tags_with_data_test) < 1): 
                raise ValueError('No results')
                # Iterate through the <a> tags and extract information
            for a_tag in a_tags_with_data_test:
                company = {}
                href = a_tag.get_attribute('href')
                review_count_element = a_tag.find_element(By.CSS_SELECTOR, 'h3[data-test="cell-Reviews-count"]').text
                company["reviewUrl"], company["reviewCount"] = href, review_count_element
                companies.append(company)
            with open(COMPANIES_FILE, 'a') as f:
                for company in companies:
                    f.write(f"{company}\n")
        except ValueError as error:
            # Write failure to the log file
            with open(LOG_PATH, "a") as f:
                f.write(
                    str(industry_number)
                    + "    Page: "
                    + str(pagenumber)
                    + "  E: "
                    + str(error)
                    + f"\n")
            continue
    driver.quit()
    return companies


# Create a thread worker
def thread_worker():
    while True:
        try:
            industry_number, page_max = queue.get(timeout=2)  # Add a timeout for safe exit
            scrape_industry_page(industry_number, page_max)
            queue.task_done()
        except:
            # If an exception occurs (including queue.Empty), exit the loop
            break

# Create a queue and thread pool
queue = Queue()
for i in range(NUM_THREADS):
    t = threading.Thread(target=thread_worker)
    t.daemon = True
    t.start()


# Enqueue tasks to the queue
for industry_number, page_max in industry_page_array:
    queue.put((industry_number, page_max))

# Wait for all tasks to finish
queue.join()
