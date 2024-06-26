from enum import Enum

from attr import define, field
from cmt_website.status.units import Radian


class DomeState(Enum):
    """Tracks state of the telescope's dome
    Absent: There is no dome
    Stopped: Motionless, no input
    Rotating: Rotating into target position
    Homing: Seeking dome's home"""

    OFFLINE = -1
    ABSENT = 0
    STOPPED = 1
    ROTATING = 2
    HOMING = 3


class ShutterState(Enum):
    """Tracks state of dome's shutter
    Absent: There is no shutter
    Idle: Not moving, position unknown
    Opening: Shutter is opening
    Closing: Shutter is closing
    Open: Shutter is open
    Closed: Shutter is closed"""

    OFFLINE = -1
    ABSENT = 0
    IDLE = 1
    OPENING = 2
    CLOSING = 3
    OPEN = 4
    CLOSED = 5


@define
class Dome:
    """Dataclass for the Dome's status, tracking tells us if the dome is tracking the telescope's direction"""

    state: DomeState = field(converter=DomeState)
    shutterstate: ShutterState = field(converter=ShutterState)
    tracking: bool = field(converter=bool)
    azimuth: Radian = field(converter=Radian)
