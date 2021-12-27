from enum import Enum

from attr import define, field


class TelescopeState(Enum):
    """State of the telescope
    Stopped: Not updating, motionless
    Hunting: Searching for target ra/dec then tracking
    Tracking: Tracking object at target ra/dec
    Slewing: Searching for target ra/dec, then stopping
    Homing: Finding home positions
    Limiting: Finding limit positions"""

    STOPPED = 1
    HUNTING = 2
    TRACKING = 3
    SLEWING = 4
    HOMING = 5
    LIMITING = 6


@define
class Telescope:
    """Dataclass for the telescope's status."""

    state: TelescopeState = field()
    ra: float = field()
    dec: float = field()
    target_ra: float = field()
    target_dec: float = field()
