import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def download_book(url, filename, folder='books'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    filepath = os.path.join(folder, filename)
    if response.status_code == 200:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return filepath
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


def get_content(id, url):
    cover_url = urljoin(url, 'b{id}/'.format(id=id))
    response = requests.get(cover_url, allow_redirects=False)
    response.raise_for_status()
    if response.status_code != 200:
        return [None, None, None]

    soup = BeautifulSoup(response.text, 'lxml')

    title = soup.find('h1').text.split('::')[0].strip()
    filename = sanitize_filename('{id}. {title}.txt'.format(id=id, title=title))

    img = soup.find('div', class_='bookimage').find('img')['src']
    split_img_name = img.split('/')
    img_name = sanitize_filename(split_img_name[len(split_img_name) - 1].strip())
    img_url = urljoin(url, img)

    return [filename, img_url, img_name]


if __name__ == '__main__':
    try:
        for id in range(1, 11):
            url = 'https://tululu.org'
            download_url = urljoin(url, 'txt.php?id={id}/'.format(id=id))
            filename, img_url, img_name = get_content(id, url)
            if filename:
                filepath = download_book(download_url, filename)
            # print('filename =', filename)
            # print('img_url =', img_url)

            if img_url:
                img_path = download_img(img_url, img_name)
                # print('img_path =', img_path)

            # print('filepath =', filepath, end='\n\n')

    except requests.exceptions.MissingSchema as err:
        print('Invalid link to book')
