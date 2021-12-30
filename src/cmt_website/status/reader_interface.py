from abc import ABC, abstractproperty

from cmt_website.status.dome import Dome
from cmt_website.status.telescope import Telescope


class StatusReaderInterface(ABC):
    """Generic status reader to make all additional status readers uniform"""

    @abstractproperty
    def telescope(self) -> Telescope:
        """Returns current telescope status"""
        raise NotImplementedError

    @abstractproperty
    def dome(self) -> Dome:
        """Returns current dome status"""
        raise NotImplementedError
