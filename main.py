import tweepy
import requests
import os
from os import environ

import time
from time import sleep

import json

from PIL import Image
import schedule

from datetime import datetime
from datetime import date

PAGES = 604
PAGES = PAGES + 1

CONSUMER_KEY = environ['YOUR_CONSUMER_KEY']
CONSUMER_SECRET = environ['YOUR_CONSUMER_SECRET']

ACCESS_TOKEN = environ['YOUR_ACCESS_KEY']
ACCESS_TOKEN_SECRET = environ['YOUR_ACCESS_SECRET']

def get_day():
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)
        return data["day"]

def days_between():
    first = datetime.strptime("2022-11-1", "%Y-%m-%d")
    today = datetime.strptime(str(date.today()), "%Y-%m-%d")
    return abs((first - today).days)

def increment_day():
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)
    with open("data.json", "w") as jsonFile:
        day = ( data["day"] + 1 ) % PAGES
        day = 1 if day == 0 else day
        data["day"] =  day
        json.dump(data, jsonFile)

def delete_downloaded_image(page):
    if os.path.exists(page):
        os.remove(page)
    else:
        print("The file does not exist")

def download_image(page):
    response = requests.get("http://www.hadota.net/photos/quran/musshaf1/"+ str(page) +".png")
    file = open(str(page)+".png", "wb")
    file.write(response.content)
    file.close()

def change_image_to_jpg(page):
    image = str(page)+".png"
    base = os.path.splitext(image)[0]
    os.rename(image, base + '.jpg')

def convert_to_jpg(page):
    im1 = Image.open(str(page)+'.png').convert('RGB')
    im1.save(str(page)+'.jpg')


def tweet(day):
    message = "#QuranPageEveryDay  #Page"+str(day)
    api.update_with_media(str(day)+".jpg", status=message) 

def process_image(day):
    download_image(day)
    convert_to_jpg(day)
    delete_downloaded_image(str(day)+".png")

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth)

def tweet_today_page():
    #day = get_day()
    day = days_between()
    process_image(day)
    tweet(day)
    increment_day()
    delete_downloaded_image(str(day)+".jpg")
    print(str(datetime.now()))

# def ttttt():
#     api.update_status("test from heroku at : "+str(datetime.now())) 

schedule.every().day.at("12:52").do(tweet_today_page)
# schedule.every(20).seconds.do(ttttt)

print(days_between())

while(1):
    schedule.run_pending()
    time.sleep(1)