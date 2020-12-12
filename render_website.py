import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import os
from pathlib import Path


def on_reload():
    with open(Path('library_contents') / 'descriptions.json', 'r', encoding='utf8') as file:
        books = json.load(file)

    list_books = list(chunked(books, 2))
    book_pages = list(chunked(list_books, 5))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')
    page_directory = 'pages'
    os.makedirs(page_directory, exist_ok=True)

    for i, book_page in enumerate(book_pages, start=1):
        rendered_page = template.render(
            book_list=book_page,
            current_page=i,
            page_count=len(book_pages)
        )
        with open(Path(page_directory) / 'index{}.html'.format(i), 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    server = Server()
    on_reload()
    server.watch('template.html', on_reload)
    server.serve(root=Path('pages') / 'index1.html')


if __name__ == '__main__':
    main()
