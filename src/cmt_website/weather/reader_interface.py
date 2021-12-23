from abc import ABC, abstractmethod

import pandas as pd


class WeatherReaderInterface(ABC):
    """Standard interface for data reader from any weather source"""

    @abstractmethod
    def read(self) -> pd.DataFrame:
        raise NotImplementedError
