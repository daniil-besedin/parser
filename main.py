import requests


def download_book(url, file_name):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(response.text)


if __name__ == '__main__':
    try:
        url = 'https://tululu.org/txt.php?id=32168'
        file_name = 'book.txt'
        download_book(url, file_name)
    except requests.exceptions.MissingSchema as err:
        print('Invalid link to book')
