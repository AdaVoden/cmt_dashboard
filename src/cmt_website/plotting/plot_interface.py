from abc import ABC, abstractproperty


class PlottingInterface(ABC):
    @abstractproperty
    def temperature(self):
        raise NotImplementedError

    @abstractproperty
    def wind_rose(self):
        raise NotImplementedError

    @abstractproperty
    def humidity(self):
        raise NotImplementedError

    @abstractproperty
    def pressure(self):
        raise NotImplementedError

    @abstractproperty
    def sqm(self):
        raise NotImplementedError
