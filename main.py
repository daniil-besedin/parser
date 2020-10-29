import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json
import argparse


def download_book(url, filename, folder='books'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    book_path = os.path.join(folder, filename)

    if response.status_code == 200:
        with open(book_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return book_path
    return None


def download_img(url, filename, folder='imgs'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    img_path = os.path.join(folder, filename)

    if response.status_code == 200:
        with open(img_path, 'wb') as img:
            img.write(response.content)
        return img_path
    return None


def get_content(id, url, book_description):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    title_and_author_selector = 'h1'
    title_and_author = soup.select_one(title_and_author_selector).text.split('::')
    title = title_and_author[0].strip()
    book_description['title'] = title
    filename = sanitize_filename('{title}.txt'.format(title=title))
    if filename:
        download_url = urljoin(base_url, 'txt.php?id={id}/'.format(id=id))
        filepath = download_book(download_url, filename)
        book_description['book_path'] = filepath

    author = title_and_author[1].strip()
    book_description['author'] = author

    img_selector = 'div.bookimage img'
    img = soup.select_one(img_selector)['src']
    split_img_name = img.split('/')
    img_name = sanitize_filename(split_img_name[len(split_img_name) - 1].strip())
    img_url = urljoin(url, img)
    img_path = download_img(img_url, img_name)
    book_description['img_src'] = img_path

    comments_selector = 'div.texts'
    html_comments = soup.select(comments_selector)
    comments = {}
    for comment in html_comments:
        author_selector = 'b'
        author = comment.select_one(author_selector).text
        comment_text_selector = 'span.black'
        comment_text = comment.select_one(comment_text_selector).text
        comments[author] = comment_text
    book_description['comments'] = comments

    genres_selector = 'span.d_book a'
    html_genres = soup.select(genres_selector)
    genres = []
    for html_genre in html_genres:
        genres.append(html_genre.text)
    book_description['genres'] = genres


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', default=1)
    parser.add_argument('--end_page', default=702)

    return parser


if __name__ == '__main__':
    try:
        parser = create_parser()
        args = parser.parse_args()

        base_url = 'https://tululu.org'
        template_genre_url = 'https://tululu.org/l55/{page}'
        start_page = int(args.start_page)
        end_page = int(args.end_page)
        book_descriptions = []

        for page in range(start_page, end_page):
            genre_page_url = template_genre_url.format(page=page)
            response = requests.get(genre_page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            books_selector = 'table.d_book'
            books = soup.select(books_selector)

            for book in books:
                book_description = {}

                url_selector = 'a'
                url = book.select_one(url_selector)['href']
                id = url.strip('/b')
                book_url = urljoin(base_url, url)
                get_content(id, book_url, book_description)

                book_descriptions.append(book_description)
                print(book_url)

        with open('descriptions.json', 'w', encoding='utf8') as file:
            json.dump(book_descriptions, file, ensure_ascii=False)

    except requests.exceptions.MissingSchema as err:
        print(err)
    except requests.exceptions.HTTPError as err:
        print(err)
    except ValueError as err:
        print('You did not enter a number')
