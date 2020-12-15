import json
import unittest
from pathlib import Path


class TestBasic(unittest.TestCase):
    def setUp(self):
        with open(Path('../library_contents') / 'descriptions.json', 'r', encoding='utf8') as file:
            self.books = json.load(file)

    def test_books_count(self):
        self.assertNotEqual(len(self.books), 0)
        self.assertEqual(len(self.books), 25)

    def test_existence_of_book(self):
        index = 0
        self.assertEqual(self.books[index]['title'], 'Алиби')
        self.assertEqual(self.books[index]['author'], 'ИВАНОВ Сергей')
        self.assertEqual(self.books[index]['book_path'], 'library_contents/books/Алиби_id=239.txt')
        self.assertEqual(self.books[index]['img_src'], 'library_contents/images/239_239.jpg')

        index = 1
        self.assertEqual(self.books[index]['title'], "Бич небесный")
        self.assertEqual(self.books[index]['author'], "Стерлинг Брюс")
        self.assertEqual(self.books[index]['book_path'], 'library_contents/books/Бич небесный_id=550.txt')
        self.assertEqual(self.books[index]['img_src'], 'library_contents/images/550_550.jpg')

        index = 2
        self.assertEqual(self.books[index]['title'], "Цена посвящения: Серый Ангел")
        self.assertEqual(self.books[index]['author'], "Маркеев Олег Георгиевич")
        self.assertEqual(self.books[index]['book_path'], 'library_contents/books/Цена посвящения Время Зверя_id=769.txt')
        self.assertEqual(self.books[index]['img_src'], 'library_contents/images/769_769.jpg')

        index = 3
        self.assertEqual(self.books[index]['title'], "Цена посвящения: Время Зверя")
        self.assertEqual(self.books[index]['author'], "Маркеев Олег Георгиевич")
        self.assertEqual(self.books[index]['book_path'], 'library_contents/books/Бич небесный_id=550.txt')
        self.assertEqual(self.books[index]['img_src'], 'library_contents/images/550_550.jpg')

        index = 4
        self.assertEqual(self.books[index]['title'], "Дело Джен, или Эйра немилосердия")
        self.assertEqual(self.books[index]['author'], "Fforde Jasper")
        self.assertEqual(self.books[index]['book_path'], 'library_contents/books/Цена посвящения Серый Ангел_id=768.txt')
        self.assertEqual(self.books[index]['img_src'], 'library_contents/images/768_768.jpg')


if __name__ == '__main__':
    unittest.main()
