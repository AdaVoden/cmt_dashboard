from abc import ABC, abstractproperty


class PlottingInterface(ABC):
    @abstractproperty
    def temperature(self):
        raise NotImplementedError

    @abstractproperty
    def wind_speed(self):
        raise NotImplementedError

    @abstractproperty
    def wind_direction(self):
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
