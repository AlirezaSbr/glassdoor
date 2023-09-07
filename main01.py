from selenium.webdriver.chrome.options import Options
import selenium.webdriver as uc

# import selenium.webdriver as uc
import cookie
import url as u
import reviwes
import xlsxwriter
from datetime import datetime as time
# import winsound
# frequency = 500  # Set Frequency To 2500 Hertz
# duration = 2000  # Set Duration To 1000 ms == 1 second

DRIVER_PATH = "venv/Media/chromedriver"
COOKIE_PATH = "venv/Media/Cookie.txt"
LOG_PATH = "venv/Media/Log.txt"
url = input("Enter URL:")
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
driver.refresh()
urlData = u.urlParse(url)
EXCEL_PATH = "venv/Media"+ urlData["companyName"] + ".xls"

maxReviewsPageNumber = reviwes.maxReviewsPageNumber(driver)

employerReviewDic = [
    "isLegal",
    "employer",
    "reviewId",
    "companyId",
    "companyName",
    "reviewId",
    "reviewDateTime",
    "ratingOverall",
    "ratingWorkLifeBalance",
    "ratingCultureAndValues",
    "ratingDiversityAndInclusion",
    "ratingSeniorLeadership",
    "ratingCareerOpportunities",
    "ratingCompensationAndBenefits",
    "ratingRecommendToFriend",
    "ratingBusinessOutlook",
    "ratingCeo",
    "isCurrentJob",
    "employmentStatus",
    "location",
    "originalLanguageId",
    "lengthOfEmployment",
    "jobEndingYear",
    "jobTitle",
    "pros",
    "prosOriginal",
    "cons",
    "consOriginal",
    "summary",
    "summaryOriginal",
    "advice",
    "adviceOriginal"
]
  # List object calls by index, but the dict object calls items randomly

reviwesData = []

for reviewPage in range(1, maxReviewsPageNumber+1 ):
    url = u.urlCreate(
        companyId=urlData["companyId"],
        companyName=urlData["companyName"],
        pageNumber=reviewPage,
        urlType="Review",
    )

    try:
        driver.get(url)
        pageSource = driver.page_source

        if pageSource.find(""""reviews":[{"__""") < 0:
            driver.refresh()
            pageSource = driver.page_source

        reviwesDataPerPage = reviwes.getReviewsBypageSource(
            pageSource=pageSource,
            companyId=urlData["companyId"],
            companyName=urlData["companyName"],
        )
        reviwesData.extend(reviwesDataPerPage)
        with open(LOG_PATH, "a") as f:
            f.write(
                "OK     "
                + str(reviewPage)
                + " of "
                + str(maxReviewsPageNumber)
                + "    "
                + str(time.now())
                + f"\n"
            )


    except:
        with open(LOG_PATH, "a") as f:
            f.write(
                "NotOk  "
                + str(reviewPage)
                + " of "
                + str(maxReviewsPageNumber)
                + "    "
                + str(time.now())
                + f"\n"
            )
            # winsound.Beep(frequency, duration)
            continue

workBook = xlsxwriter.Workbook(EXCEL_PATH)
workSheet = workBook.add_worksheet(
    "firstSheet"
)  # Or leave it blank. The default name is "Sheet 1"
first_row = 0
for header in employerReviewDic:
    col = employerReviewDic.index(header)  # We are keeping order.
    workSheet.write(
        first_row, col, header
    )  # We have written first row which is the header of worksheet also.
for review in reviwesData:
    for _key, _value in review.items():
        if _key in employerReviewDic:
            col = employerReviewDic.index(_key)
            workSheet.write(reviwesData.index(review) + 1, col, _value)
        else:
            pass
workBook.close()
driver.quit()
# winsound.Beep(frequency, duration)
