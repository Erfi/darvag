import unittest
from src.database.text_database import TextDatabase

class TextDatabaseTest(unittest.TestCase):

    def test_text_database_init(self):
        filename = ''
        db = TextDatabase(filename)
        self.assertIsNotNone(db)


if __name__ == "__main__":
    unittest.main()