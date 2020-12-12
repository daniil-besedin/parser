# Парсер книг с сайта tululu.org && своя онлайн библиотека

Проект позволяет забирать данные о книгах с сайта [tululu.org](https://tululu.org/). Далее компануем данные и выгружаем на сайт [free-libary](https://daniil-besedin.github.io/parser/pages/index1.html). Чтобы открыть сайт перейдите по ссылке [free-libary](https://daniil-besedin.github.io/parser/pages/index1.html).

### Как установить

Для работы с проектом необходим Python 3 и библиотеки из файла `requirements.txt`.

Сделать клон проекта `git clone https://github.com/daniil-besedin/parser.git`.

Создать виртуальное окружение `python -m venv --copies ./virtualenv`.

Активировать виртуальное окружение `sourse ./virtualenv/Scripts/activate.bat`.

Установить зависимости проекта `pip install -r requirements.txt`.

### Аргументы

`--start_page` - страница с которой начинается загрузка.

`--end_page` - страница на которой завершается загрузка.

`--dest_folder` - указание корневой директории под книги и их обложки.

`--skip_imgs` - флаг отменяющий загрузку обложек.

`--skip_txt` - флаг отменяющий загрузку книг.

`--json_path` - путь к *.json файлу с результатами.

### Как запустить парсер

Пример `python main.py --start_page 1 --end_page 2 --dest_folder main --skip_imgs --skip_txt --json_path main\descriptions.json`.

### Как пересобрать сайт с новыми книгами

Нужно перезапустить `render_website.py`. Пример `python render_website.py`. После запушить изменения на GitHub и через несколько секунд github-pages их применит к вашему сайту.

### Наша онлайн библиотека

Ссылка на сайт [free-libary](https://daniil-besedin.github.io/parser/pages/index1.html)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
