from attr import define, field
from cmt_website.status.dome import Dome, DomeState, ShutterState
from cmt_website.status.reader_interface import StatusReaderInterface
from cmt_website.status.telescope import Telescope, TelescopeState
from cmt_website.status.units import Radian

error_dome = Dome(
    state=DomeState(-1),
    shutterstate=ShutterState(-1),
    tracking=False,
    azimuth=Radian(0),
)
error_telescope = Telescope(
    state=TelescopeState(-1),
    ra=Radian(0),
    dec=Radian(0),
    altitude=Radian(0),
    azimuth=Radian(0),
    hour_angle=Radian(0),
)


@define(slots=True)
class ErrorStatus(StatusReaderInterface):
    @property
    def telescope(self) -> Telescope:
        return error_telescope

    @property
    def dome(self) -> Dome:
        return error_dome
