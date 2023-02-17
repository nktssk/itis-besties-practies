from bs4 import BeautifulSoup
from bs4.element import Comment

import os
import shutil
import urllib.request

from source.Crawler import Crawler

if __name__ == '__main__':
    base_url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html"
    spider = Crawler(base_url, nested_link_class)
    spider.start_parsing()
