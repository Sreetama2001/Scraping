from bs4 import BeautifulSoup as bs
import requests

def getSiteData(url):
    response = requests.get(url)
    if response.status_code == 200:
        siteData = bs(response.content, "html5lib")
        return siteData
    return None

def getFeaturedStory(siteData):
    pass


if __name__=="__main__":
    print("...")
    targetUrl = "https://www.ndtv.com/"
    print(getSiteData(targetUrl))