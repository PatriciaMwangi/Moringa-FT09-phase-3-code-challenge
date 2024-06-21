import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

   # def test_article_creation(self):
  #      article = Article(1, "Test Title", "Test Content", 1, 1)
   #     self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly")
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_valid_title(self):
        article = Article(title="Tech Trends", content="Latest in tech", author_id=1, magazine_id=1)
        self.assertEqual(article.title, "Tech Trends")

    def test_invalid_title_length(self):
        with self.assertRaises(ValueError):
            Article(title="Tech", content="Latest in tech", author_id=1, magazine_id=1)
        
        with self.assertRaises(ValueError):
            Article(title="T" * 51, content="Latest in tech", author_id=1, magazine_id=1)

    def test_invalid_title_type(self):
        with self.assertRaises(ValueError):
            Article(title=12345, content="Latest in tech", author_id=1, magazine_id=1)

    def test_title_already_set(self):
        article = Article(title="Tech Trends", content="Latest in tech", author_id=1, magazine_id=1)
        with self.assertRaises(ValueError):
            article.title = "New Title"

if __name__ == "__main__":
    unittest.main()
