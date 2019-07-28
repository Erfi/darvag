from src.database.base import Base
from api_paths import DATA_PATH
from data_classes import Dictionary_Entry
from api_exceptions import DatabaseInsertException

class TextDatabase(Base):

    def __init__(self):
        self.english_to_german_path = DATA_PATH / 'english_to_german.csv'
        self.german_to_english_path = DATA_PATH / 'german_to_english.csv'

    def select(self, item):
        pass

    def insert(self, item: Dictionary_Entry):
        try:
            filename = self.english_to_german_path if item.from_lang == 'english' else self.german_to_english_path
            with open(filename, 'a') as f:
                s = f'{item.key},{item.value},{item.example}\n'
                f.write(s)
        except Exception as e:
            raise DatabaseInsertException(f'Could not insert {item}. {e}')

    def update(self, item):
        pass

    def delete(self, item):
        pass
