from astropy.coordinates.angles import Longitude
from attr import define, field
from astropy.coordinates.earth import EarthLocation
from astropy.time import Time
from astropy.units import deg
from datetime import datetime, timezone


@define
class ObservatoryTime:
    location: EarthLocation = field()

    @staticmethod
    def _as_hms(dt: datetime) -> str:
        return dt.strftime("%H:%M:%S")

    @property
    def timezone(self) -> str:
        return str(datetime.now(timezone.utc).astimezone().tzinfo)

    @property
    def utc(self) -> str:
        return self._as_hms(datetime.now(timezone.utc))

    @property
    def local(self) -> str:
        return self._as_hms(datetime.now(timezone.utc).astimezone())

    @property
    def date(self) -> str:
        return datetime.today().strftime("%d/%m/%y")

    @property
    def lst(self) -> str:
        astro_time = Time(datetime.now(timezone.utc), location=self.location)
        lst = astro_time.sidereal_time(kind="apparent")
        return lst.to_string(decimal=False, sep=":", precision=0, pad=True)


def make_time(longitude: float, latitude: float, height: float) -> ObservatoryTime:
    """ObservatoryTime factory using longitude, latitude and height as inputs into the time holder

    Parameters
    ----------
    longitude : float
        Longitude of observatory, in degrees
    latitude : float
        Latitude of observatory, in degrees
    height : float
        Elevation of observatory, in meters

    Returns
    -------
    ObservatoryTime
        Time object to return all local time to the location of observatory,
        along with UTC

    """
    if longitude < -180 or longitude > 180:
        raise ValueError(
            f"Expected longitude to be between -180 and 180 degrees, received {longitude}"
        )
    if latitude < -90 or latitude > 90:
        raise ValueError(
            f"Expected latitude to be between -90 and 90 degrees, received {latitude}"
        )
    if height < 0:
        raise ValueError(f"Expected height to be at least 0, received {height}")
    longitude = Longitude(angle=longitude * deg, wrap_angle=180 * deg)
    location = EarthLocation.from_geodetic(lon=longitude, lat=latitude, height=height)
    o_time = ObservatoryTime(location)
    return o_time
