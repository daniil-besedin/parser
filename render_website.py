import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked
from pprint import pprint


def on_reload():
    with open('main/descriptions.json', 'r', encoding='utf8') as file:
        books = json.load(file)
    list_books = list(chunked(books, 2))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        list_books=list_books
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    server = Server()
    on_reload()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()
