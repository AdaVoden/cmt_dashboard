from abc import ABC, abstractmethod


class DataReader(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError


class AsyncDataReader(DataReader):
    @abstractmethod
    async def read(self):
        raise NotImplementedError


class DataWriter(ABC):
    @abstractmethod
    def write(self, data):
        raise NotImplementedError


class AsyncDataWriter(ABC):
    @abstractmethod
    async def write(self, data):
        raise NotImplementedError
