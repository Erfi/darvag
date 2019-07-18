from abc import ABC, abstractmethod


class Base(ABC):

    @abstractmethod
    def select(self, item):
        pass

    @abstractmethod
    def insert(self, item):
        pass

    @abstractmethod
    def update(self, item):
        pass

    @abstractmethod
    def delete(self, item):
        pass
