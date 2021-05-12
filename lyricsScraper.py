from bs4 import BeautifulSoup
import requests
import certifi
import re
import json

file = open('songs.json', 'r')
try:
    allSongs = json.loads(file.read())
except:
    allSongs = {"songs": {}}

file.close()
file = open('songs.json', 'w')

with open('top50.txt', 'r') as songFile:
    songList = songFile.readlines()
    for x in range(len(songList)):
        songList[x] = eval(
            repr(songList[x].replace(" - ", ' ').replace("\n", "")))
        re.sub(r'\W+', '', songList[x])

urlrapid = "https://genius.p.rapidapi.com/search"


headers = {
    'x-rapidapi-key': "4e2948119fmsh2450827ec8904e7p1f240ajsna47a0370583e",
    'x-rapidapi-host': "genius.p.rapidapi.com"
}
x = 0
while x in range(len(songList)):

    querystring = {"q": songList[x]}
    try:
        response = requests.request(
            "GET", urlrapid, headers=headers, params=querystring)

        song = {}

        song['title'] = response.json(
        )['response']['hits'][0]['result']['title'].replace("\u00a0", " ")
        song['title_with_featured'] = response.json(
        )['response']['hits'][0]['result']['title_with_featured'].replace("\u00a0", " ")
        song['artist'] = response.json(
        )['response']['hits'][0]['result']['primary_artist']['name'].replace("\u00a0", " ")
        song['full_title'] = response.json(
        )['response']['hits'][0]['result']['full_title'].replace("\u00a0", " ")
        re.sub(r'\W+', '', song['title'])
        re.sub(r'\W+', '', song['title_with_featured'])
        re.sub(r'\W+', '', song['artist'])
        re.sub(r'\W+', '', song['full_title'])

        print(song)

    except:
        x += 1
        continue

    try:
        song = allSongs['songs'][song['full_title']]
    except:

        url = response.json()['response']['hits'][0]['result']['url']

        page = requests.get(url)

        soup = BeautifulSoup(page.content, features="lxml")

        allLyrics = soup.findAll(
            "div", class_="Lyrics__Container-sc-1ynbvzw-2")

        lyrics = ""

        for para in allLyrics:

            cleanr = re.compile('<.*?>')
            cleantext = re.sub(cleanr, '\n', str(para))

            lyrics += cleantext.strip()

        lyricsNew = lyrics.replace('\n\n', ' ').replace('[', '\n\n[')
        re.sub(r'\W+', '', lyricsNew)

        if lyricsNew == "":
            continue

        song['lyrics'] = lyricsNew

        allSongs['songs'][song['full_title']] = song
    finally:
        pass

    x += 1


file.write(json.dumps(allSongs, indent=4))
file.close()
