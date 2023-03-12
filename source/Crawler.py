from bs4 import BeautifulSoup
from bs4.element import Comment

import os
import shutil
import urllib.request


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


class Crawler:

    def __init__(self,
                 base_url,
                 nested_link_class,
                 max_pages_count=100,
                 min_words_count=500,
                 output_directory="output/pages/",
                 output_filename="index.txt"):
        self.__base_url = base_url
        self.__nested_link_class = nested_link_class
        self.__max_pages_count = max_pages_count
        self.__min_words_count = min_words_count
        self.__output_directory = output_directory
        self.__output_filename = output_filename
        self.__current_page_index = 0
        self.__queue = []
        self.__parsed_urls = set()

    def start_parsing(self):
        self.__prepare_output_directory()
        self.__queue.append(self.__base_url)

        while self.__queue and self.__current_page_index < self.__max_pages_count:
            url = self.__queue.pop()
            html = get_html(url)
            soup = BeautifulSoup(html, 'html.parser')

            print('Start handling %d %s ...' % (self.__current_page_index, url))

            if self.__check_text_size(soup):
                self.__save_html(self.__current_page_index, url, html)
                self.__parsed_urls.add(url)
                self.__current_page_index += 1
                nested_links = list(filter(self.__is_handled, self.__get_nested_links(soup)))
                self.__queue.extend(nested_links)

        print("Done!")

    def __prepare_output_directory(self):
        try:
            shutil.rmtree(self.__output_directory)
            os.mkdir(self.__output_directory)
        except OSError:
            print("Creation of the directory %s failed" % self.__output_directory)
        else:
            print("Successfully created the directory '%s' " % self.__output_directory)

    def __is_handled(self, url):
        return not (url in self.__parsed_urls)

    def __get_nested_links(self, soup):
        internal_references = soup.find_all("a", class_=self.__nested_link_class)
        links = list(set([self.__base_url + item['href'] for item in internal_references]))
        return links

    def __check_text_size(self, soup):
        size = len(soup.text.split())
        return size >= self.__min_words_count

    def __save_html(self, index, url, html):
        html_filename_path = self.__output_directory + str(index) + ".txt"
        html_file = open(html_filename_path, "wb")
        html_file.write(html)
        html_file.close()

        output_filename_path = self.__output_directory + self.__output_filename

        with open(output_filename_path, 'a') as file:
            line = str(index) + " – " + url + "\n"
            file.write(line)
