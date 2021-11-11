import json, requests, pandas as pd
from requests.models import Response
from lxml import html
from dateutil.parser import parse


class ndtv:
    def __init__(self):
        self.newsCategories = {
            "latest": "https://www.ndtv.com/latest",
            "india": "https://www.ndtv.com/india",
            "world": "https://www.ndtv.com/world-news",
            "science": "https://www.ndtv.com/science",
            "business": "https://www.ndtv.com/business/latest",
            "entertainment": "https://www.ndtv.com/entertainment/latest",
            "offbeat": "https://www.ndtv.com/offbeat",
            "crypto": "https://www.ndtv.com/business/cryptocurrency/news",
        }

    def getSiteData(self, siteUrl):
        response = requests.get(siteUrl)
        if response.status_code == 200:
            siteData = html.fromstring(response.content)
            return siteData
        return None

    def getPageCount(self, siteData):
        pageCountXpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
        try:
            pageCount = int(siteData.xpath(pageCountXpath + "/text()")[0])
        except:
            pageCount = 1
        return pageCount

    def getHeadline(self, pageData, newsId):
        try:
            headline = pageData.xpath(
                f"(//h2[contains(@class,'newsHdng')]/a)[{newsId}]/text()"
            )[0]
        except IndexError:
            headline = None
        return headline

    def getNewsUrl(self, headlineObject):
        try:
            newsUrl = headlineObject.get("href")
        except:
            newsUrl = None
        return newsUrl

    def getDescription(self, pageData, newsId):
        descriptionXpath = f"(//h2[contains(@class,'newsHdng')]/a)[{newsId}]/parent::h2/following-sibling::p/text()"
        try:
            description = pageData.xpath(descriptionXpath)[0]
        except IndexError:
            description = None
        return description

    def getImageUrl(self, pageData, newsId):
        imgXpath = f"(//h2[contains(@class,'newsHdng')]/a)[{newsId}]/parent::h2/parent::div/preceding-sibling::div/a/img"
        try:
            imageUrl = pageData.xpath(imgXpath)[0].get("src")
        except IndexError:
            imageUrl = None
        return imageUrl

    def getDate(self, pageData, newsId):
        dateXpath = f"(//h2[contains(@class,'newsHdng')]/a)[{newsId}]/parent::h2/following-sibling::span/text()"
        try:
            dateSpan = pageData.xpath(dateXpath)
            date = None
            for item in dateSpan:
                try:
                    date = parse(item, fuzzy=True).date()
                except:
                    pass
        except IndexError:
            date = None
        return date

    def getCatagoryNews(self, newsCategory, catagoryUrl):
        newsDf = pd.DataFrame(
            columns=[
                "category",
                "headline",
                "description",
                "url",
                "imageUrl",
                "postedDate",
            ]
        )

        siteData = self.getSiteData(catagoryUrl)
        pageCount = self.getPageCount(siteData)

        headline = []
        description = []
        url = []
        imageUrl = []
        date = []

        for page in range(1, pageCount + 1):
            pageData = self.getSiteData(siteUrl=f"{catagoryUrl}/page-{page}")
            headlineObjects = pageData.xpath("//h2[contains(@class,'newsHdng')]/a")

            for newsId in range(1, len(headlineObjects) + 1):
                headline.append(self.getHeadline(pageData, newsId))
                description.append(self.getDescription(pageData, newsId))
                url.append(self.getNewsUrl(headlineObjects[newsId - 1]))
                imageUrl.append(self.getImageUrl(pageData, newsId))
                date.append(self.getDate(pageData, newsId))

        newsDf["headline"] = headline
        newsDf["description"] = description
        newsDf["url"] = url
        newsDf["imageUrl"] = imageUrl
        newsDf["postedDate"] = date
        newsDf = newsDf.assign(category=newsCategory)

        return newsDf


finalData = pd.DataFrame()

ndtv = ndtv()
# finalData = ndtv.getCatagoryNews("latest", "https://www.ndtv.com/latest")
for category in ndtv.newsCategories:
    df = ndtv.getCatagoryNews(category, ndtv.newsCategories[category])
    finalData = finalData.append(df, ignore_index=True)

finalData.to_csv("newResult.csv", index=False, header=True)
