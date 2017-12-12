import praw
import requests
from tesserocr import PyTessBaseAPI
import urllib.request
import ssl
from PIL import Image
import glob
import enchant
from enchant.checker import SpellChecker
import re

url_list = []
image_url_list = []
image_list = []
image_list = []
enchant_dict = enchant.Dict("en_US")
chkr = SpellChecker("en_US")
counter = 0
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
iteration = 0
size = 1800, 3200

reddit = praw.Reddit('bot1')

subreddit = reddit.subreddit("getmotivated")

for submission in subreddit.hot(limit=20):
    if not submission.is_self:
        url_list.append(submission.url)

for url in url_list:
    response = requests.head(url)
    if 'image' in response.headers.get('content-type'):
        image_url_list.append(url)

for image_url in image_url_list:
    filename = "file" + str(counter) + ".jpg"
    print(image_url)
    image = urllib.request.urlretrieve(image_url, filename, context.get_ca_certs())
    image_list.append(filename)
    counter += 1

for filename in glob.glob('*.jpg'):
    wrong_words = 0
    image = Image.open(filename)
    image.resize(size, Image.ANTIALIAS)
    image.save(filename)
    with PyTessBaseAPI() as api:
        print ("Iteration: " + str(iteration))
        try:
            api.SetImageFile(filename)
        except TypeError:
            print ("Caught a TypeError from: " + str(filename))
        word_confidences = api.AllWordConfidences()
        average_confidence = sum(word_confidences) / len(word_confidences)
        print (average_confidence)
        print (word_confidences)
        if average_confidence > 80:
            text = api.GetUTF8Text()
            chkr.set_text(text)
            print(text)
            for err in chkr:
                suggestions = enchant_dict.suggest(err.word)
                if suggestions:
                    chkr.replace(suggestions[0])
            text = chkr.get_text()
            chkr.set_text(text)
            for err in chkr:
                wrong_words = wrong_words + 1
            print ("There are " + str(wrong_words) + " wrong words.")
            new_average = wrong_words / len(word_confidences)
            if new_average < 20:
                print (text)
        else:
            print("Confidence is not high enough for this image. \n")
        iteration += 1

print("Image list is: " + str(len(image_list)) + " images long.")


'''
with PyTessBaseAPI() as api:
    for filename in image_list:
        print ("Iteration: " + str(iteration))
        try:
            api.SetImageFile(filename)
        except TypeError:
            print ("Caught a TypeError from: " + str(filename))
        word_confidences = api.AllWordConfidences()
        print (word_confidences)
        if all(confidence >= 80 for confidence in word_confidences):
            print (api.GetUTF8Text())
        else:
            print("Confidence is not high enough for this image. \n")
        iteration += 1
'''