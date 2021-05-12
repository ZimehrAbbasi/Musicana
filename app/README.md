
# Musicana

Musicana uses IBM's world class tone recognition api as well as twitter's handy api and combines it into the most sophiisticated twitter bot the world has ever seen. When tweeted at, Musicana uses the song, analyses its lyrics, gathers its tones, cross-references it agaist thousands of songs, and tweets you back with the song that most closely resembles your mood.

```python
Current_status: Asleep
```

## Imports

```python
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
```

## Usage

Tweet at the account and include the song in the tweet. The Twitter API will lcate the user, and reply with a song similar to the one tweeted to it with.

```python
def auth(): # Authentication
def create_url(): 
def get_params(): # Getting header params
def create_headers(bearer_token): # Creating header
def connect_to_endpoint(url, headers, params): # Coonnect to twitter api
def getList(dict): # dict to list
def analyze(text): # Analyze songs sentiment analysis
def main(): # driver
```
