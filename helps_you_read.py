import praw
import requests
from tesserocr import PyTessBaseAPI
import urllib.request
import ssl
from PIL import Image
import glob

url_list = []
image_url_list = []
image_list = []
image_list = []
counter = 0
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
iteration = 0
size = 1500, 1200

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
    image = Image.open(filename)
    image.thumbnail(size)
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
        if average_confidence > 68:
            print (api.GetUTF8Text())
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