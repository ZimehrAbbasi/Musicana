##
# @Author, Zimehr Abbasi
# This module extracts all the songs from the billboard top 100 chart periodically to update its database
##

from bs4 import BeautifulSoup
import requests
import certifi
import re

url = "https://www.billboard.com/charts/year-end/2010/hot-100-songs"

page = requests.get(url)

soup = BeautifulSoup(page.content, features="lxml")

allSongs = soup.findAll("div", class_="ye-chart-item__title")

for x in allSongs:
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '\n', str(x)).replace(
        "\n\n", " ").replace("\t", "").replace("\n", ":").replace(":        :", "")
    print(cleantext)
