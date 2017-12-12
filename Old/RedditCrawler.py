'''
Created on Dec 10, 2017

@author: colemank95
'''


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


class RedditCrawlwer:

    '''
    METHOD: constructor
    ARGS:
    '''

    def __init__(self):

        self._url_list = []

        self._image_url_list = []

        self._reddit = reddit = praw.Reddit('bot1')

        self._subreddit = reddit.subreddit("getmotivated")

        self._counter = 0

        self._text_array = []

        self._spellchecked_array = []

        self._context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

        self._enchant_dict = enchant.Dict("en_US")

        self._chkr = SpellChecker("en_US")

        self._size = 1800, 3200

        self._wrong_words = 0

        self._word_conferences = []

        self._new_average = 0

    '''
    METHOD: fetchUrls
    ARGS:
    DESCRIPTION: - called to fetch urls from reddit that contain an image.
    RETURN: nothing
    '''

    def fetchUrls(self):

        for submission in self._subreddit.hot(limit=20):
            if not self._submission.is_self:
                self._url_list.append(self._submission.url)

        for url in self._url_list:
            response = requests.head(url)
            if 'image' in response.headers.get('content-type'):
                self._image_url_list.append(url)

    '''
    METHOD: downloadImages
    ARGS:
    DESCRIPTION: - called to download the images from the fetched urls
    RETURN: nothing
    '''

    def downloadImages(self):

        for image_url in self._image_url_list:
            filename = "file" + str(self._counter) + ".jpg"
            print(image_url)
            image = urllib.request.urlretrieve(
                image_url, filename, context.get_ca_certs())
            self._image_list.append(filename)
            self._counter += 1

    '''
    METHOD: parseText
    ARGS:
    DESCRIPTION: - parses the text in images
    RETURN: nothing
    '''

    def parseText(self):

        for filename in glob.glob('*.jpg'):
            image = Image.open(filename)
            image.resize(self._size, Image.ANTIALIAS)
            image.save(filename)
            with PyTessBaseAPI() as api:
                try:
                    api.SetImageFile(filename)
                except TypeError:
                    print ("Caught a TypeError from: " + str(filename))

                text = api.GetUTF8Text()

                self._text_array.append(text)

    '''
    METHOD: checkSpelling
    ARGS:
    DESCRIPTION: - spellchecks the text to try to improve accuracy
    RETURN: nothing
    '''

    def checkSpelling(self):

        for text in self._text_array:
            self._chkr.set_text(text)
            print(text)
            for err in self._chkr:
                suggestions = self._enchant_dict.suggest(err.word)
                if suggestions:
                    self._chkr.replace(suggestions[0])
            text = self._chkr.get_text()
            self._chkr.set_text(text)
            for err in self._chkr:
                self._wrong_words = self._wrong_words + 1
            print ("There are " + str(self._wrong_words) + " wrong words.")
            self._spellchecked_array.append(text)
