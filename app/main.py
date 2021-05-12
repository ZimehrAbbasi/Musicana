import json
import os
import requests
import tweepy
from bs4 import BeautifulSoup
import requests
import certifi
import re
import random
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import time

apikey = 'aiEwC0TZqi7ZYksP4Ez0qAzTPI5xHSpS8P0ghG3IPyPg'
url = 'https://api.eu-gb.tone-analyzer.watson.cloud.ibm.com/instances/8f660912-fdc5-4d14-914a-e37d0141399a'

authenticator = IAMAuthenticator(apikey)
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
tone_analyzer.set_service_url(url)

APIKey = 'zth0DrGbZUHup6doL0RCXS439'
APIKeySecret = 'E8BQi1oOJar2DR18Fsc9LNhF7rFQtjp2J3bRXpQ3kPY4bkZcu1'
AccessToken = '1271352921477677056-WD4FWbqzhI2dydQTwuC9iTnqXNDQ6N'
AccessTokenSecret = 'Mi4SmOJNOiWoxvQi9UQO5pPyMSRpU7r6b1qIvM1Hd9urc'
BEARER_TOKEN = r'AAAAAAAAAAAAAAAAAAAAAGCwMgEAAAAAjpv%2FZ303rQLEzwTmqaC0BcI8LTQ%3DHuSmEwcn8Gtl6cCEkO1qZs1xvOGkW7mUQulzAthHQq8WH4Ew3p'

file = open('songs.json', 'r')
try:
    allSongs = json.loads(file.read())
except:
    allSongs = {"songs": {}}
file.close()

urlrapid = "https://genius.p.rapidapi.com/search"


headersrapid = {
    'x-rapidapi-key': "4e2948119fmsh2450827ec8904e7p1f240ajsna47a0370583e",
    'x-rapidapi-host': "genius.p.rapidapi.com"
}

auth = tweepy.OAuthHandler(APIKey, APIKeySecret)
auth.set_access_token(AccessToken, AccessTokenSecret)

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)

user_id = 1271352921477677056
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return BEARER_TOKEN


def create_url():
    # Replace with user ID below
    return "https://api.twitter.com/2/users/{}/mentions".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "author_id"}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def getList(dict):
    list = []
    for key in dict.keys():
        list.append(key)

    return list


def analyze(text):
    querystring = {"q": text}
    try:
        response = requests.request(
            "GET", urlrapid, headers=headersrapid, params=querystring)

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

        # print(song)

    except:
        return "Error"

    try:
        song = allSongs['songs'][song['full_title']]
        #print("Checkpoint 1")
    except:
        #print("Checkpoint 1.5")
        urlmid = response.json()['response']['hits'][0]['result']['url']
        #print("Checkpoint 2")
        page = requests.get(urlmid)
        #print("Checkpoint 3")
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
            return analyze(text)

        song['lyrics'] = lyricsNew

        allSongs['songs'][song['full_title']] = song

        lyrics = song['lyrics'].replace('\n', " ")
        tone_analysis = tone_analyzer.tone(
            {'text': lyrics},
            content_type='application/json'
        ).get_result()
        name = song['full_title']
        allSongs['songs'][name]['tone'] = []
        for tone in tone_analysis['document_tone']["tones"]:
            allSongs['songs'][name]['tone'].append(
                {tone["tone_name"]: tone["score"]})
            try:
                allSongs['tones'][tone["tone_name"]].append(name)
            except:
                allSongs['tones'][tone["tone_name"]] = []
                allSongs['tones'][tone["tone_name"]].append(name)

        #print("Checkpoint 5")

    tone = getList(song["tone"][-1])[0]

    if len(tone) != 0:
        return allSongs["tones"][tone][-1]


def main():
    bearer_token = auth()
    headers = create_headers(bearer_token)
    params = get_params()
    url = create_url()
    json_response = connect_to_endpoint(url, headers, params)
    data = json_response
    #print(json.dumps(data, indent=4, sort_keys=True))
    newtextFile = open('newest.txt', 'r')
    latestread = newtextFile.read()
    newtextFile.close()

    newTweets = []
    if latestread != data['meta']["newest_id"]:
        i = 0
        while data["data"][i]["id"] != latestread:
            newTweets.append(data["data"][i])
            i += 1
        with open("newest.txt", 'w') as textFile:
            textFile.write(data['meta']["newest_id"])
    else:
        print("No new tweets...")
        return

    for tweet in newTweets:
        text = tweet["text"].split("@ZimehrsPA ")[-1]
        user = api.get_user(tweet["author_id"])
        # returns list of songs with similar tone
        reco = analyze(text)
        if reco != "Error":
            api.update_status(
                f"@{user.screen_name} may I suggest {reco}", tweet["id"])
        else:
            api.update_status(
                f"@{user.screen_name} Error occured", tweet["id"])
        print(f"Replied to @{user.screen_name}")


if __name__ == "__main__":
    while True:
        main()
        time.sleep(20)
