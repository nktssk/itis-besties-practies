from crawler import Crawler

import requests
from bs4 import BeautifulSoup
import re
import os
import pymorphy2
import nltk
from stop_words import get_stop_words

nltk.download('punkt')

# Инициализируем анализатор морфологии
morph = pymorphy2.MorphAnalyzer()

stop_words = get_stop_words('ru')


def get_contents():
    # Создаем директорию для файлов, если она не существует
    if not os.path.exists('output'):
        os.makedirs('output')

    # Список страниц для загрузки
    urls = []

    # Создаем файл index.txt
    with open('index.txt', 'w', encoding='utf-8') as f:
        for i in range(1, 101):
            urls.append(f"https://habr.com/ru/post/{i}")
        for i, url in enumerate(urls):
            # Получаем содержимое страницы
            response = requests.get(url)
            content = response.content

            # Парсим содержимое страницы и сохраняем его в файл
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text().lower()
            text = re.sub(r'\s+', ' ', text)  # удаляем лишние пробелы и переносы строк
            filename = f'output/{i + 1}.txt'
            with open(filename, 'w', encoding='utf-8') as page_file:
                page_file.write(text)

            # Записываем номер файла и ссылку на страницу в файл index.txt
            f.write(f'{i + 1}. {url}\n')


# Функция для получения списка токенов из файла
def get_tokens(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        # Удаляем лишние символы
        text = re.sub(r'\W+', ' ', text)
        # Токенизируем текст
        tokens = nltk.word_tokenize(text)
        # Отфильтровываем стоп-слова и "мусор"
        tokens = [token for token in tokens if token not in stop_words and re.match(r'^[а-яА-Я]+$', token) and not any(
            char.isdigit() for char in token)]
        # Лемматизируем токены
        # lemmas = [morph.parse(token)[0].normal_form for token in tokens]
        # Оставляем только уникальные леммы
        unique_lemmas = set(tokens)
        return list(unique_lemmas)


def get_lemmas():
    # Создаем пустой список токенов
    tokens = []

    # Перебираем все файлы в директории output
    for filename in os.listdir('output'):
        # Получаем список токенов из файла
        file_tokens = get_tokens('output/' + filename)
        # Добавляем токены в общий список
        tokens += file_tokens

    tokens = set(tokens)
    # Группируем токены по леммам
    lemmas = {}
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        if lemma in lemmas:
            lemmas[lemma].append(token)
        else:
            lemmas[lemma] = [token]

    with open('tokens.txt', 'w', encoding='utf-8') as f:
        for token in sorted(tokens):
            f.write(token + ' ')

    with open('grouped_tokens.txt', 'w', encoding='utf-8') as f:
        for lemma in sorted(lemmas.keys()):
            f.write(lemma + ': ' + ', '.join(lemmas[lemma]) + '\n')


if __name__ == '__main__':
    get_contents()
    # get_lemmas()
