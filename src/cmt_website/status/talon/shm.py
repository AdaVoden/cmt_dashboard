from struct import Struct

import sysv_ipc as sysv
from attr import define, field
from cmt_website.status.dome import Dome, DomeState, ShutterState
from cmt_website.status.telescope import Telescope, TelescopeState

# Formats of structs defined for Talon shared memory
# Used to read from shared memory buffer
TELESCOPE_POSITIONS_FORMAT = "16d"
STATUS_FORMAT = "5ici3?2d2i"

# Named tuple definitions for above formats to assist with readability
# EOD means Epoch of Date
@define(slots=True)
class TelescopePosition:
    J2000_ra: float = field(converter=float)
    J2000_dec: float = field(converter=float)
    EOD_ra: float = field(converter=float)
    EOD_ha: float = field(converter=float)
    EOD_dec: float = field(converter=float)
    altitude: float = field(converter=float)
    azimuth: float = field(converter=float)
    parallactic_angle: float = field(converter=float)
    target_J2000_ra: float = field(converter=float)
    target_J2000_dec: float = field(converter=float)
    target_EOD_ra: float = field(converter=float)
    target_EOD_ha: float = field(converter=float)
    target_EOD_dec: float = field(converter=float)
    target_altitude: float = field(converter=float)
    target_azimuth: float = field(converter=float)
    target_parallactic_angle: float = field(converter=float)


@define(slots=True)
class Status:
    telescope_state: TelescopeState = field(converter=TelescopeState)
    ccd_temp_status: int = field(converter=int)
    cam_state: int = field(converter=int)
    cam_temp: float = field(converter=float)
    target_camp_temp: float = field(converter=float)
    filter: str = field(converter=str)
    lights: int = field(converter=int)
    autofocus: bool = field(converter=bool)
    jogging: bool = field(converter=bool)
    autodome: bool = field(converter=bool)
    dome_azimuth: float = field(converter=float)
    target_dome_azimuth: float = field(converter=float)
    domestate: DomeState = field(converter=DomeState)
    shutterstate: ShutterState = field(converter=ShutterState)


@define
class SHMStatusReader:
    """Using a given hex key, initializes and mediates a connection to a Linux shared memory segment that's used by the Talon/OCAAS system to share information between different daemons"""

    # Buffer offsets from 0, used to read specific pieces of data from the shared memory
    # Calculated from the sizes the non-changing partings of telstatshm.h in libmisc
    telescope_offset: int = field(default=88)  # bytes
    status_offset: int = field(default=920)  # bytes
    SHM_hex_key: str = field(default="0x4e56361a")
    SHM_dec_key: int = field(init=False)
    _shared_memory: sysv.SharedMemory = field(init=False)
    _status: Status = field(init=False)
    _telescope_position: TelescopePosition = field(init=False)
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
        self._telescope_position = TelescopePosition(
            t_struct.unpack_from(shm_buffer, offset=t_offset)
        )
        self._status = Status(s_struct.unpack_from(shm_buffer, offset=s_offset))

    def read_telescope(self):
        self._read_all()
        position = self._telescope_position
        status = self._status
        return Telescope(
            state=status.telescope_state,
            ra=position.J2000_ra,
            dec=position.J2000_dec,
            hour_angle=position.EOD_ha,
            azimuth=position.azimuth,
            altitude=position.altitude,
        )

    def read_dome(self):
        self._read_all()
        status = self._status
        return Dome(
            state=status.domestate,
            shutterstate=status.shutterstate,
            tracking=status.autodome,
            azimuth=status.dome_azimuth,
        )
