from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from math import ceil


def maxReviewsPageNumber(driver: Chrome):
    try:
        paginationFooter = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".paginationFooter"))
        ).text
    except:
        return None
    paginationFooter = (driver.find_element(By.CSS_SELECTOR, ".paginationFooter")).text
    words = paginationFooter.split(" ")
    totalRevieNumber = int(words[5].replace(",", ""))
    maxReviewsPageNumber = ceil(totalRevieNumber / 10)
    return maxReviewsPageNumber


def getReviewsBypageSource(pageSource, companyName, companyId):
    pageSourceReview = (
        pageSource[
            pageSource.find(""""reviews":[{"__""") : pageSource.find(
                """},"featuredReviewIdForEmployer("""
            )
        ][len(""""reviews":""") + 2 :]
        .replace("true", "True")
        .replace("false", "False")
        .replace("null", "None")
        .replace('"', "")
    )

    reviewsList = pageSourceReview.split("},{")

    review_list = []
    for review in reviewsList:
        if (
            review.find("__typename:EmployerReview") != -1
        ):  # reviewType == EmployerReview
            reviewDict = {}
            revList = review.replace("{", "").replace("}", "").split(",")
            for rev in revList:
                try:
                    if rev.count(":") > 1:
                        key, value = rev.split(":", 1)
                        reviewDict[key] = value
                    else:
                        key, value = rev.split(":")
                        reviewDict[key] = value
                    if key == "isLanguageMismatch":
                        break
                except:
                    pass
            reviewDict["companyId"],reviewDict["companyName"]= companyId, companyName
            review_list.append(reviewDict)
        else:
            pass

    return review_list
