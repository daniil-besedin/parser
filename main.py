import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin
import json
import argparse
from time import sleep
from pathlib import PurePosixPath


def download_book(url, filename, folder='books', main_folder=''):
    folder = PurePosixPath(main_folder) / folder
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, allow_redirects=False, verify=False)
    response.raise_for_status()
    book_path = str(folder / filename)
    print(book_path)

    if response.status_code == 200:
        with open(book_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return book_path
    return None


def download_img(url, filename, folder='images', main_folder=''):
    folder = PurePosixPath(main_folder) / folder
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, allow_redirects=False, verify=False)
    response.raise_for_status()
    img_path = str(folder / filename)

    if response.status_code == 200:
        with open(img_path, 'wb') as img:
            img.write(response.content)
        return img_path
    return None


def get_content(id, url, book_description, base_url, main_folder='', skip_imgs=False, skip_txt=False):
    response = requests.get(url, allow_redirects=False, verify=False)
    response.raise_for_status()
    if response.status_code != 200:
        return
    soup = BeautifulSoup(response.text, 'lxml')

    title_and_author_selector = 'h1'
    title_and_author = soup.select_one(title_and_author_selector).text.split('::')
    title = title_and_author[0].strip()
    book_description['title'] = title
    filename = sanitize_filename('{title}_id={id}.txt'.format(title=title, id=id))
    if not skip_txt:
        download_url = urljoin(base_url, 'txt.php?id={id}/'.format(id=id))
        filepath = download_book(download_url, filename, main_folder=main_folder)
        book_description['book_path'] = filepath
        print()

    author = title_and_author[1].strip()
    book_description['author'] = author

    img_selector = 'div.bookimage img'
    img = soup.select_one(img_selector)['src']
    split_img_name = img.split('/')
    img_name = sanitize_filename(split_img_name[len(split_img_name) - 1].strip())
    img_name = id + '_' + img_name
    img_url = urljoin(url, img)
    if not skip_imgs:
        os.makedirs(main_folder, exist_ok=True)
        img_path = download_img(img_url, img_name, main_folder=main_folder)
        book_description['img_src'] = img_path

    comments_selector = 'div.texts'
    html_comments = soup.select(comments_selector)
    author_selector = 'b'
    comment_text_selector = 'span.black'
    comments = {key.select_one(author_selector).text: value.select_one(comment_text_selector).text for key, value in
                zip(html_comments, html_comments)}
    book_description['comments'] = comments

    genres_selector = 'span.d_book a'
    html_genres = soup.select(genres_selector)
    genres = [html_genre.text for html_genre in html_genres]
    book_description['genres'] = genres


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_page', type=int, default=1)
    parser.add_argument('--end_page', type=int, default=702)
    parser.add_argument('--dest_folder', default='resources')
    parser.add_argument('--skip_imgs', action='store_true', default=False)
    parser.add_argument('--skip_txt', action='store_true', default=False)
    parser.add_argument('--json_path', default='resources')

    return parser


def main():
    requests.packages.urllib3.disable_warnings()
    parser = create_parser()
    args = parser.parse_args()

    main_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    json_path = args.json_path
    base_url = 'https://tululu.org'
    template_genre_url = 'https://tululu.org/l55/{page}'
    start_page = args.start_page
    end_page = args.end_page
    book_descriptions = []

    for page in range(start_page, end_page):
        genre_page_url = template_genre_url.format(page=page)

        try:
            response = requests.get(genre_page_url, allow_redirects=False, verify=False)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            continue
        except requests.exceptions.ConnectionError as err:
            print(err)
            sleep(5)
            continue

        if response.status_code != 200:
            print('Страниы по адресу {} не существует'.format(genre_page_url))
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        books_selector = 'table.d_book'
        books = soup.select(books_selector)

        for book in books:
            book_description = {}

            url_selector = 'a'
            url = book.select_one(url_selector)['href']
            id = url.strip('/b')
            book_url = urljoin(base_url, url)

            try:
                get_content(id, book_url, book_description, base_url, main_folder=main_folder, skip_imgs=skip_imgs,
                            skip_txt=skip_txt)
            except requests.exceptions.HTTPError as err:
                print(err)
                continue
            except requests.exceptions.ConnectionError as err:
                print(err)
                sleep(5)
                continue

            book_descriptions.append(book_description)
            print(book_url)

    with open(json_path, 'w', encoding='utf8') as file:
        json.dump(book_descriptions, file, ensure_ascii=False)


if __name__ == '__main__':
    main()
