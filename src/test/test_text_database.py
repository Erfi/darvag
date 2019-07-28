import unittest
from src.database.text_database import TextDatabase
from data_classes import Dictionary_Entry


class TextDatabaseTest(unittest.TestCase):

    def setUp(self):
        self.db = TextDatabase()

    def test_text_database_init(self):
        db = TextDatabase()
        self.assertIsNotNone(db)

    def test_insert(self):
        entry = Dictionary_Entry(from_lang='english', to_lang='german', key='Cold', value='kalt',
                                 example='Die wasser ist kalt.')
        self.db.insert(entry)


if __name__ == "__main__":
    unittest.main()
