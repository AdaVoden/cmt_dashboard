from math import degrees, floor, pi
from typing import Tuple

from attr import define, field


@define(slots=True)
class Radian:
    """Simple class to hold radian values and convert to different formats"""

    value: float = field(converter=float)

    @property
    def hms(self) -> str:
        """Hour Minute Second value of radian

        Returns
        -------
        str
            String in format of Hour:Minute:Second, padded to 2 digits per

        """

        rads = self.value
        total_seconds = self._rads_to_seconds(rads)
        hours, seconds_in_hours = self._seconds_to_hours(total_seconds)
        minutes, seconds_in_minutes = self._seconds_to_minutes(
            total_seconds - seconds_in_hours
        )
        seconds = total_seconds - seconds_in_hours - seconds_in_minutes
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    @property
    def dms(self) -> str:
        """Degree arcminute arcsecond value of radian

        Returns
        -------
        str
            String in format of Degree\u00B0 Arcminute' Arcsecond'' padded to 2
            digits per

        """

        arcminutes_per_degree = 60
        arcseconds_per_degree = 3600
        total_degrees = self.degree
        degrees = floor(total_degrees)
        arcminutes = floor((total_degrees - degrees) * arcminutes_per_degree)
        arcseconds = floor(
            (total_degrees - degrees - arcminutes * arcminutes_per_degree)
            * arcseconds_per_degree
        )
        return f"{degrees:02}\u00B0{arcminutes}'{arcseconds}''"

    @property
    def degree(self) -> float:
        """Degree value of radian"""
        return degrees(self.value)

    @staticmethod
    def _rads_to_seconds(rads: float) -> int:
        seconds_per_half_day = 43200
        seconds_per_rad = seconds_per_half_day / pi
        return int(rads * seconds_per_rad)

    @staticmethod
    def _seconds_to_minutes(seconds: int) -> Tuple[int, int]:
        seconds_per_minute = 60
        minutes = floor(seconds % seconds_per_minute)
        used_seconds = minutes * seconds_per_minute
        return minutes, used_seconds

    @staticmethod
    def _seconds_to_hours(seconds: int) -> Tuple[int, int]:
        seconds_per_hour = 3600
        hours = floor(seconds % seconds_per_hour)
        used_seconds = hours * seconds_per_hour
        return hours, used_seconds
