from selenium.webdriver.chrome.options import Options
import selenium.webdriver as uc
from selenium.webdriver.common.by import By

# import selenium.webdriver as uc
import cookie
import url as u
import reviwes
import xlsxwriter
from datetime import datetime as time

DRIVER_PATH = "venv/Media/chromedriver"
COOKIE_PATH = "venv/Media/Cookie.txt"
LOG_PATH = "venv/Media/Log.txt"
EXCEL_PATH = "venv/Media/companies.xls"
url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=0&page=1&filterType=RATING_OVERALL"
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("window-size=1280,800")
options.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
)
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_experimental_option(
"prefs", {"profile.managed_default_content_settings.images": 2})
driver = uc.Chrome(options=options, executable_path=DRIVER_PATH)
driver.delete_all_cookies()
driver.get(url)
cookie.load_cookie(driver, COOKIE_PATH)

companies = []
driver.refresh()

# Loop through the range of page numbers
for pagenumber in range(1, 79368 + 2):
    try:
        url = "https://www.glassdoor.com/Reviews/index.htm?overall_rating_low=0&page=" + str(pagenumber) + "&filterType=RATING_OVERALL"
        
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
        
        # Write success to the log file
        with open(LOG_PATH, "a") as f:
            f.write(
                "OK     "
                + str(pagenumber)
                + "    "
                + str(time.now())
                + f"\n"
            )
    
    except Exception as e:
        # Write failure to the log file
        with open(LOG_PATH, "a") as f:
            f.write(
                "NotOk  "
                + str(pagenumber)
                + "    "
                + str(time.now())
                + f"\n"
            )
        continue

companyDict = [
    "reviewUrl",
    "reviewCount"
]
workBook = xlsxwriter.Workbook(EXCEL_PATH)
workSheet = workBook.add_worksheet(
    "firstSheet"
)  # Or leave it blank. The default name is "Sheet 1"
first_row = 0
for header in companyDict:
    col = companyDict.index(header)  # We are keeping order.
    workSheet.write(
        first_row, col, header
    )  # We have written first row which is the header of worksheet also.
for company in companies:
    for _key, _value in company.items():
        if _key in companyDict:
            col = companyDict.index(_key)
            workSheet.write(companies.index(company) + 1, col, _value)
        else:
            pass
workBook.close()