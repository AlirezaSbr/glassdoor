
def urlParse(url):
    sampleUrl= str('https://www.glassdoor.com/Reviews/')
    companyName=(url[len(sampleUrl):url.find('-Reviews')])
    companyId=(url[url.find('Reviews-')+len('Reviews-'):url.find('.htm')])
    pageNumber=1
    if companyId.find('_P')>0:
        pageNumber=companyId[companyId.find('_')+2:]
        companyId=companyId[:companyId.find('_')]
    return({
        'companyName': companyName,
        'companyId':  companyId,
        'pageNumber':  pageNumber
    })

def urlCreate(companyId,companyName,urlType ,pageNumber = 0, ):
    if urlType == 'Review':
        url='https://www.glassdoor.com/Reviews/'+ companyName + '-Reviews-' + companyId + '_P' + str(pageNumber) + '.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng'
        return url
    if urlType == 'CompanyDetail':
        url='https://www.glassdoor.com/Overview/Working-at-'+ companyName + '-EI_I' + companyId + '.htm'
        return url




