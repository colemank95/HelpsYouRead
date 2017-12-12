from .RedditCrawler import RedditCrawler


def main():
    application = RedditCrawler()
    application.fetchUrls()
    application.downloadImages()
    application.parseText()
    application.checkSpelling()
    text_array = application.getText()

    for text in text_array:
        print(text)
