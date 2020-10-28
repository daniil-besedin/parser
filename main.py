import requests
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


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


def get_file_name(id):
    cover_url = 'https://tululu.org/b{id}/'.format(id=id)
    response = requests.get(cover_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text.split('::')[0].strip()
    return sanitize_filename('{id}. {title}.txt'.format(id=id, title=title))


if __name__ == '__main__':
    try:
        for id in range(1, 11):
            url = 'https://tululu.org/txt.php?id={id}'.format(id=id)
            filename = get_file_name(id)
            filepath = download_book(url, filename)
            print(filepath)
    except requests.exceptions.MissingSchema as err:
        print('Invalid link to book')
