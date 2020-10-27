import requests
import os


def download_book(url, file_name):
    response = requests.get(url, allow_redirects=False)
    response.raise_for_status()
    if response.status_code == 200:
        with open('folder_0/' + file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)


if __name__ == '__main__':
    path = 'folder_0'
    os.makedirs(path, exist_ok=True)
    try:
        for id in range(1, 11):
            url = 'https://tululu.org/txt.php?id={id}'.format(id=id)
            file_name = 'id{id}.txt'.format(id=id)
            download_book(url, file_name)
    except requests.exceptions.MissingSchema as err:
        print('Invalid link to book')
