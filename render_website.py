import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import os
from pprint import pprint


def on_reload():
    with open('main/descriptions.json', 'r', encoding='utf8') as file:
        books = json.load(file)

    list_books = list(chunked(books, 2))
    book_pages = list(chunked(list_books, 5))
    print(len(book_pages))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    page_directory = 'pages'
    os.makedirs(page_directory, exist_ok=True)

    for i, book_page in enumerate(book_pages):
        rendered_page = template.render(
            list_books=book_page
        )
        with open(os.path.join(page_directory, 'index{}.html'.format(i + 1)), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    server = Server()
    on_reload()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
