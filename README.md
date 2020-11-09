# Парсер книг с сайта tululu.org

Проект позволяет забирать данные о книгах с сайта [tululu.org](https://tululu.org/).

### Как установить

Для работы с проектом необходим Python 3 и библиотеки из файла `requirements.txt`.

Сделать клон проекта `git clone https://github.com/daniil-besedin/parser.git`.

Создать виртуальное окружение `python -m venv --copies ./virtualenv`.

Активировать виртуальное окружение `./virtualenv/Scripts/activate.bat`.

Установить зависимости проекта `pip install -r requirements.txt`.

### Аргументы

`--start_page` - страница с которой начинается загрузка.

`--end_page` - страница на которой завершается загрузка.

`--dest_folder` - указание корневой директории под книги и их обложки.

`--skip_imgs` - флаг отменяющий загрузку обложек. Принимает `yes` и `no`.

`--skip_txt` - флаг отменяющий загрузку книг. Принимает `yes` и `no`.

`--json_path` - путь к *.json файлу с результатами.

### Как запустить

Пример `main.py --start_page 1 --end_page 2 --dest_folder main --skip_imgs yes --skip_txt yes --json_path main\descriptions.json`.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
