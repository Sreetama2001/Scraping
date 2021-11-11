import pandas as pd
import requests
import json
from lxml import html
from dateutil.parser import parse


def scrap_page_and_fetch_news_data(category, news_page_url):
    news_df = pd.DataFrame(
        columns=[
            "category",
            "headline",
            "description",
            "url",
            "image_url",
            "posted_date",
        ]
    )

    # finding the last entry in the pagination to find the total pages present for the particoular category
    last_page_xpath = "//div[contains(@class,'listng_pagntn clear')]/a[contains(@class,'btnLnk arrowBtn next')]/preceding-sibling::a[position()=1]"
    page = requests.get(news_page_url)
    tree = html.fromstring(page.content)
    try:
        total_pages = tree.xpath(last_page_xpath + "/text()")[0]
    except:
        total_pages = 1

    headline_list = []
    description_list = []
    image_url_list = []
    url_list = []
    posted_date_list = []

    for page in range(1, int(total_pages) + 1):

        page_url = f"{news_page_url}/page-{page}"
        page = requests.get(page_url)
        tree = html.fromstring(page.content)
        news_header_xpath = "//h2[contains(@class,'newsHdng')]/a"
        headline_elements = tree.xpath(news_header_xpath)

        for i in range(1, int(len(headline_elements)) + 1):
            try:
                news_headline = tree.xpath(f"({news_header_xpath})[{i}]/text()")[
                    0
                ]  # *headline
            except IndexError:
                news_headline = None

            try:
                news_url = headline_elements[i - 1].get("href")  # *url
            except:
                news_url = None

            description_xpath = (
                f"({news_header_xpath})[{i}]/parent::h2/following-sibling::p/text()"
            )
            try:
                description = tree.xpath(description_xpath)[0]  # *description
            except IndexError:
                description = None

            img_xpath = f"({news_header_xpath})[{i}]/parent::h2/parent::div/preceding-sibling::div/a/img"
            try:
                img_url = tree.xpath(img_xpath)[0].get("src")  # *image_url
            except IndexError:
                img_url = None

            posted_date_xpath = (
                f"({news_header_xpath})[{i}]/parent::h2/following-sibling::span/text()"
            )
            try:
                posted_date_span = tree.xpath(posted_date_xpath)  # *posted date
                posted_date = None
                for text in posted_date_span:
                    try:
                        posted_date = parse(text, fuzzy=True).date()
                    except:
                        pass
            except IndexError:
                posted_date = None

            headline_list.append(news_headline)
            description_list.append(description)
            image_url_list.append(img_url)
            url_list.append(news_url)
            posted_date_list.append(posted_date)

    news_df["headline"] = headline_list
    news_df["description"] = description_list
    news_df["url"] = url_list
    news_df["image_url"] = image_url_list
    news_df["posted_date"] = posted_date_list
    news_df = news_df.assign(category=category)

    return news_df


# main_news_dataframe = pd.DataFrame(
#     columns=["category", "headline", "description", "url", "image_url", "posted_date"]
# )

# available_categories = {"latest": "https://www.ndtv.com/latest"}

available_categories = {
    "latest": "https://www.ndtv.com/latest",
    "india": "https://www.ndtv.com/india",
    "world": "https://www.ndtv.com/world-news",
    "science": "https://www.ndtv.com/science",
    "business": "https://www.ndtv.com/business/latest",
    "entertainment": "https://www.ndtv.com/entertainment/latest",
    "offbeat": "https://www.ndtv.com/offbeat",
    "crypto": "https://www.ndtv.com/business/cryptocurrency/news",
}

finalData = pd.DataFrame()
for category in available_categories:
    df = scrap_page_and_fetch_news_data(
        category=category, news_page_url=available_categories[category]
    )
    finalData = finalData.append(df, ignore_index=True)

# df = scrap_page_and_fetch_news_data(
#     category="latest", news_page_url=available_categories["latest"]
# )

finalData.to_csv("result.csv", index=False, header=True)
