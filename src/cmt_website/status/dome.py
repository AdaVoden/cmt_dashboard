from enum import Enum

from attr import define, field


class DomeState(Enum):
    """Tracks state of the telescope's dome
    Absent: There is no dome
    Stopped: Motionless, no input
    Rotating: Rotating into target position
    Homing: Seeking dome's home"""

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

    ABSENT = 0
    IDLE = 1
    OPENING = 2
    CLOSING = 3
    OPEN = 4
    CLOSED = 5


@define
class Dome:
    """Dataclass for the Dome's status, tracking tells us if the dome is tracking the telescope's direction"""

    state: DomeState = field()
    shutterstate: ShutterState = field()
    tracking: bool = field()
    azimuth: float = field()
    target_azimuth: float = field()
