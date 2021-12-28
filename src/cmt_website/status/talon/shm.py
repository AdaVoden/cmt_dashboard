from collections import namedtuple
from struct import Struct
from typing import NamedTuple

import sysv_ipc as sysv
from attr import define, field
from cmt_website.status.dome import Dome, DomeState, ShutterState
from cmt_website.status.telescope import Telescope, TelescopeState

# from cmt_website.status.dome import Dome, DomeState, ShutterState
# from cmt_website.status.telescope import Telescope, TelescopeState

# Formats of structs defined for Talon shared memory
# Used to read from shared memory buffer
TELESCOPE_POSITIONS_FORMAT = "16d"
STATUS_FORMAT = "5ici3?2d2i"

# Named tuple definitions for above formats to assist with readability
# EOD means Epoch of Date
Telescope_Position = namedtuple(
    "Telescope_Positions",
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
    "Observatory_Status",
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
    telescope_offset: int = field(default=88)  # bytes
    status_offset: int = field(default=920)  # bytes
    SHM_hex_key: str = field(default="0x4e56361a")
    SHM_dec_key: int = field(init=False)
    _shared_memory: sysv.SharedMemory = field(init=False)
    _status: Status = field(init=False)
    _telescope_position: Telescope_Position = field(init=False)
    _status_struct: Struct = field(init=False)
    _telescope_struct: Struct = field(init=False)

    def __attrs_post_init__(self):
        self.SHM_dec_key = int(self.SHM_hex_key, 16)
        try:
            self._shared_memory = sysv.SharedMemory(self.SHM_dec_key)
            print(self._shared_memory)
            self._status_struct = Struct(STATUS_FORMAT)
            self._telescope_struct = Struct(TELESCOPE_POSITIONS_FORMAT)
        except sysv.ExistentialError:
            raise BufferError(
                "Unable to read shared memory, it currently does not exist."
            )

    def _read_all(self):
        shm_buffer = self._shared_memory.read()
        t_offset = self.telescope_offset
        s_offset = self.status_offset
        t_struct = self._telescope_struct
        s_struct = self._status_struct
        self._telescope_position = Telescope_Position._make(
            t_struct.unpack_from(shm_buffer, offset=t_offset)
        )
        self._status = Status._make(s_struct.unpack_from(shm_buffer, offset=s_offset))

    def read_telescope(self):
        self._read_all()
        position = self._telescope_position
        status = self._status
        print(position)
        telescope_state = TelescopeState(status.telescope_state)
        return Telescope(
            state=telescope_state,
            ra=position.J2000_ra,
            dec=position.J2000_dec,
            target_ra=position.target_J2000_ra,
            target_dec=position.target_J2000_dec,
        )

    def read_dome(self):
        self._read_all()
        status = self._status
        print(status)
        domestate = DomeState(status.domestate)
        shutterstate = ShutterState(status.shutterstate)
        return Dome(
            state=domestate,
            shutterstate=ShutterState,
            tracking=status.autodome,
            azimuth=status.dome_azimuth,
            target_azimuth=status.target_dome_azimuth,
        )
