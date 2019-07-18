from src.database.base import Base
from pathlib import Path


class TextDatabase(Base):

    def __init__(self, filepath):
        self.filepath = filepath

    def select(self, item):
        pass

    def insert(self, item):
        pass

    def update(self, item):
        pass

    def delete(self, item):
        pass



