
from selenium.webdriver.chrome.options import Options
from selenium import webdriver 
import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
import fake_useragent as UserAgent
# import selenium.webdriver as uc
import cookie
import xlsxwriter
from datetime import datetime as time
import time as tm

# Array containing [industrycode, pagenumber]
industry_page_array = [
    [200021,495,0],[200022,999,1,0],[200023,722,1,0],[200024,385,1,0],[200028,999,1,0],[200029,263,0],[200030,261],[200031,282],[200032,719],[200033,553],[200034,155],[200035,202],[200036,999],[200037,345],[200038,70],[200039,78],[200040,496],[200041,36],[200042,53],[200043,142],[200044,702],[200045,529],[200046,999],[200047,576],[200048,746],[200052,174],[200055,13],[200056,310],[200057,957],[200058,406],[200059,999],[200060,999],[200061,999],[200063,605],[200064,999],[200065,295],[200066,269],[200068,242],[200070,587],[200071,537],[200072,270],[200073,999],[200074,294],[200075,260],[200076,101],[200077,213],[200080,346],[200082,297],[200083,80],[200085,86],[200087,158],[200088,255],[200089,999],[200091,761],[200094,954],[200096,158],[200097,62],[200099,999],[200100,24],[200101,115],[200102,136],[200103,122],[200105,567],[200106,85],[200107,200],[200109,49],[200110,67],[200111,253],[200113,39],[200115,319],[200116,34],[200117,101],[200118,29],[200119,651],[200120,174],[200122,259],[200127,25],[200128,24],[200130,502],[200132,27],[200134,89],[200135,501],[200139,474],[200144,120],[200145,100],[200146,817],[200147,999],[200148,10],[200149,26],[200150,65],[200151,90],[200152,41],[200153,349],[200154,187],[200155,284],[200156,129],[200157,41],[200158,42],[200159,32],[200160,9],[200161,9],[200162,21],[200163,36],[200164,29],[200165,18],[200166,17,0]
]



DRIVER_PATH = "venv/Media/chromedriver"
COOKIE_PATH = "venv/Media/Cookie.txt"


url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=0&page=1&industry=" + str(200001) + "&filterType=RATING_OVERALL"
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=/Users/alirezasaberi/Library/Application Support/Google/Chrome/Default")
driver = uc.Chrome(options=options)
driver.delete_all_cookies()
driver.get(url)
cookie.load_cookie(driver, COOKIE_PATH)
driver.refresh()
for industryCode in range(0, len(industry_page_array) -1):
    industryNumber= industry_page_array[industryCode][0]
    pagenumberMax= industry_page_array[industryCode][1]
    log_path = "venv/Media/Log_industry(" + str(industryNumber) + ")_" + str(pagenumberMax) + ".txt"
    file_Path= "venv/Media/companies_industry(" + str(industryNumber) + ")_" + str(pagenumberMax) + ".txt"
    url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=0&page=1&industry=" + str(industryNumber) + "&filterType=RATING_OVERALL"
    try:
        open(log_path, "x")
        open(file_Path, "x")
    except:
        print()
    
    for pagenumber in range(1, pagenumberMax + 1):
        try:
            companies = []
            url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=0&page=" + str(pagenumber) + "&industry=" + str(industryNumber) + "&filterType=RATING_OVERALL"
            # Navigate to the URL
            driver.get(url)
            # Find all <a> tags with the specified attribute
            a_tags_with_data_test = driver.find_elements(By.CSS_SELECTOR, 'a[data-test="cell-Reviews-url"]')
            # Iterate through the <a> tags and extract information
            for a_tag in a_tags_with_data_test:
                company = {}
                href = a_tag.get_attribute('href')
                review_count_element = a_tag.find_element(By.CSS_SELECTOR, 'h3[data-test="cell-Reviews-count"]').text
                company["reviewUrl"], company["reviewCount"] = href, review_count_element
                companies.append(company)
            # Handle Detection
            if (len(a_tags_with_data_test) > 0):
                with open(file_Path, "a") as f:
                    for company in companies:
                        f.write(f"{company}\n") 
            else: 
                raise ValueError('No results')
            # Write success to the log file
            with open(log_path, "a") as f:
                f.write(
                    "OK     "
                    + str(pagenumber)
                    + "    "
                    + str(time.now())
                    + f"\n"
                )
        except ValueError as error:
            # Write failure to the log file
            with open(log_path, "a") as f:
                f.write(
                    str(industryNumber)
                    + "    Page: "
                    + str(pagenumber)
                    + "  E: "
                    + str(error)
                    + f"\n")
            break
    
# # Create a thread worker
# def thread_worker():
#     while True:
#         try:
#             industry_number, page_max = queue.get(timeout=2)  # Add a timeout for safe exit
#             scrap(industry_number, page_max)
#             queue.task_done()
#         except:
#             # If an exception occurs (including queue.Empty), exit the loop
#             break

# # Create a queue and thread pool
# queue = Queue()
# for i in range(NUM_THREADS):
#     t = threading.Thread(target=thread_worker)
#     t.daemon = True
#     t.start()


# # Enqueue tasks to the queue
# for industry_number, page_max in industry_page_array:
#     queue.put((industry_number, page_max))

# # Wait for all tasks to finish
# queue.join()
