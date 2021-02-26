import tweepy
import requests
import os
from time import sleep
import json
from PIL import Image



PAGES = 604
PAGES = PAGES + 1
CONSUMER_KEY ="2w0735dDwttgnqOoNlKIyk0ps"
CONSUMER_SECRET ="90jGteGMQWJAMvegDnBNT2sDwZfhW5KRQRA58sTMMe35yikbTt"

ACCESS_TOKEN = "3247968953-HMs6GCFbMjOl71FNKwliFfKUWBtZZieuwoBndiw"
ACCESS_TOKEN_SECRET = "ceL5gZkhc9XIKlchJFY5c9fE1uYM0aFQyQQykd4ptJbVm"

def get_day():
    with open("data.json", "r") as jsonFile:
        data = json.load(jsonFile)
        return data["day"]

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



while(1):
    day = get_day()
    process_image(day)
    tweet(day)
    increment_day()
    delete_downloaded_image(str(day)+".jpg")
    sleep(24*60*60)