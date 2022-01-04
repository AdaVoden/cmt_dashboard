from enum import Enum

from attr import define, field
from cmt_website.status.units import Radian


class TelescopeState(Enum):
    """State of the telescope
    Stopped: Not updating, motionless
    Hunting: Searching for target ra/dec then tracking
    Tracking: Tracking object at target ra/dec
    Slewing: Searching for target ra/dec, then stopping
    Homing: Finding home positions
    Limiting: Finding limit positions"""

    ERROR = -1
    STOPPED = 1
    HUNTING = 2
    TRACKING = 3
    SLEWING = 4
    HOMING = 5
    LIMITING = 6


@define
class Telescope:
    """Dataclass for the telescope's status."""

    state: TelescopeState = field(converter=TelescopeState)
    ra: Radian = field(converter=Radian)
    dec: Radian = field(converter=Radian)
    altitude: Radian = field(converter=Radian)
    azimuth: Radian = field(converter=Radian)
    hour_angle: Radian = field(converter=Radian)
