from enum import Enum

from attr import define, field


class DomeState(Enum):
    """Tracks state of the telescope's dome
    Absent: There is no dome
    Stopped: Motionless, no input
    Rotating: Rotating into target position
    Homing: Seeking dome's home"""

    ABSENT = 1
    STOPPED = 2
    ROTATING = 3
    HOMING = 4


class ShutterState(Enum):
    """Tracks state of dome's shutter
    Absent: There is no shutter
    Idle: Not moving, position unknown
    Opening: Shutter is opening
    Closing: Shutter is closing
    Open: Shutter is open
    Closed: Shutter is closed"""

    ABSENT = 1
    IDLE = 2
    OPENING = 3
    CLOSING = 4
    OPEN = 5
    CLOSED = 6


@define
class Dome:
    """Dataclass for the Dome's status, tracking tells us if the dome is tracking the telescope's direction"""

    state: DomeState = field()
    shutterstate: ShutterState = field()
    tracking: bool = field()
    azimuth: float = field()
    target_azimuth: float = field()
