from abc import ABC, abstractmethod


class DataReader(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError


class DataWriter(ABC):
    @abstractmethod
    def write(self, data):
        raise NotImplementedError
