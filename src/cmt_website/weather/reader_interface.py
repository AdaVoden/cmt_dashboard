from abc import ABC, abstractmethod

import pandas as pd


class WeatherNotifierWatcherInterface(ABC):
    @abstractmethod
    def notify(self):
        """On change, watcher is notified and performs some action"""
        raise NotImplementedError


class WeatherNotifierInterface(ABC):
    """Standard interface for notifying about changes to the source of a weather
    data stream"""

    @abstractmethod
    def register(self, watcher: WeatherNotifierWatcherInterface):
        """Register watcher to be notified on change"""
        raise NotImplementedError

    @abstractmethod
    def unregister(self, watcher: WeatherNotifierWatcherInterface):
        """Unregisters watcher"""
        raise NotImplementedError


class WeatherReaderInterface(ABC):
    """Standard interface for data reader from any weather source"""

    @abstractmethod
    def read(self) -> pd.DataFrame:
        raise NotImplementedError
