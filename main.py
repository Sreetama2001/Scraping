from bs4 import BeautifulSoup as bs
import requests

# with open('http://akul.me/blog/2016/beautifulsoup-cheatsheet/')
# content=html_file.read()
# print(content)
r = requests.get("http://akul.me/blog/2016/beautifulsoup-cheatsheet/")
soup = bs(r.content, "html5lib")
print(soup.prettify())
