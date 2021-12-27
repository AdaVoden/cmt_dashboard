from collections import namedtuple
from struct import unpack_from
from typing import NamedTuple

import sysv_ipc as sysv
from attr import define, field
from cmt_website.status.dome import Dome, DomeState, ShutterState
from cmt_website.status.telescope import Telescope, TelescopeState

# Formats of structs defined for Talon shared memory
# Used to read from shared memory buffer
TELESCOPE_POSITIONS_FORMAT = "16d"
STATUS_FORMAT = "5ic4i2d2i"

# Named tuple definitions for above formats to assist with readability
# EOD means Epoch of Date
Telescope_Position = namedtuple(
    "Telescope Positions",
    [
        "J2000_ra",
        "J2000_dec",
        "EOD_ra",
        "EOD_ha",
        "EOD_dec",
        "altitude",
        "azimuth",
        "parallactic_angle",
        "target_J2000_ra",
        "target_J2000_dec",
        "target_EOD_ra",
        "target_EOD_ha",
        "target_EOD_dec",
        "target_altitude",
        "target_azimuth",
        "target_parallactic_angle",
    ],
)
Status = namedtuple(
    "Observatory Status",
    [
        "telescope_state",
        "ccd_temp_status",
        "cam_state",
        "cam_temp",
        "target_cam_temp",
        "filter",
        "lights",
        "autofocus",
        "jogging",
        "autodome",
        "dome_azimuth",
        "target_dome_azimuth",
        "domestate",
        "shutterstate",
    ],
)


@define
class SHMStatusReader:
    """Using a given hex key, initializes and mediates a connection to a Linux shared memory segment that's used by the Talon/OCAAS system to share information between different daemons"""

    # Buffer offsets from 0, used to read specific pieces of data from the shared memory
    telescope_offset: int = field(default=128)  # bytes
    status_offset: int = field(default=256)  # bytes
    SHM_hex_key: str = field(default="0x4e56361a")
    SHM_dec_key: int = field(init=False)
    _shared_memory: sysv.SharedMemory = field(init=False)
    _status: Status = field(init=False)
    _telescope_position: Telescope_Position = field(init=False)

    def __attrs_post_init__(self):
        self.SHM_dec_key = int(self.SHM_hex_key, 16)
        try:
            self._shared_memory = sysv.SharedMemory(self.SHM_dec_key)
        except sysv.ExistentialError:
            raise BufferError(
                "Unable to read shared memory, it currently does not exist."
            )

    def _read_all(self):
        buffer = self._shared_memory.read()
        t_offset = self.telescope_offset
        s_offset = self.status_offset
        self._telescope_position = Telescope_Position._make(
            unpack_from(
                __format=TELESCOPE_POSITIONS_FORMAT, buffer=buffer, offset=t_offset
            )
        )
        self._status = Status._make(
            unpack_from(__format=STATUS_FORMAT, buffer=buffer, offset=s_offset)
        )

    def read_telescope(self):
        self._read_all()
        position = self._telescope_position
        status = self._status
        telescope_state = TelescopeState(status.telescope_state)
        return Telescope(
            state=telescope_state,
            ra=position.J2000_ra,
            dec=position.J2000_dec,
            target_ra=position.target_J2000_ra,
            target_dec=position.target_J2000_dec,
        )
