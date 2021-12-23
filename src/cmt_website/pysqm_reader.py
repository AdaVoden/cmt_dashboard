#!/usr/bin/env python


"""
PySQM reading program
____________________________

Copyright (c) Mireia Nievas <mnievas[at]ucm[dot]es>
Modified by Harlan Shaw <harlan.shaw@ucalgary.ca>

This file is part of PySQM.

PySQM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PySQM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PySQM.  If not, see <http://www.gnu.org/licenses/>.
____________________________
"""

import logging
import string
import time
from datetime import datetime, timedelta, timezone
from socket import AF_INET, SOCK_STREAM, socket
from typing import Iterable, List, Literal

import numpy as np
from attr import define, field


def _filtered_mean(array: Iterable[float], sigma: int = 3) -> float:
    """Calculates the sigma clipped mean of a dataset

    Parameters
    ----------
    array : Iterable[float]
        Numbers to find mean of
    sigma : int
        Standard deviations from median above which are clipped

    Returns
    -------
    float
        Sigma-clipped mean

    """

    # Our data probably contains outliers, filter them
    # Notes:
    #   Median is more robust than mean
    #    Std increases if the outliers are far away from real values.
    #    We need to limit the amount of discrepancy we want in the data (20%?).

    # We will use data masking and some operations with arrays. Convert to numpy.
    array = np.array(array)

    # Get the median and std.
    data_median = np.median(array)
    data_std = np.std(array)

    # Max discrepancy we allow.
    fixed_max_dev = 0.2 * data_median
    clip_deviation = np.min([fixed_max_dev, data_std * sigma + 0.1])

    # Create the filter (10% flux + variable factor)
    filter_values_ok = np.abs(array - data_median) <= clip_deviation
    filtered_values = array[filter_values_ok]

    # Return the mean of filtered data or the median.
    if np.size(filtered_values) == 0:
        print("Warning: High dispersion found on last measures")
        filtered_mean = data_median
    else:
        filtered_mean = np.mean(filtered_values)

    return filtered_mean


def _remove_non_digit_characters(data: str) -> str:
    """Removes all non-digit characters from a string. Allows for '.' to exist, for decimal numbers

    Parameters
    ----------
    data : str
        String to strip

    Returns
    -------
    str
        Cleaned string

    """
    chars_to_remove = set(string.printable) - set(string.digits + ".")
    cleaned = [x for x in list(data) if x not in chars_to_remove]
    return "".join(cleaned)


@define
class IPConnection:
    """Given a port and a IPv4 I.P. address, creates a context manager connection with the address at specified port"""

    ip_address: str = field(converter=str)
    port: int = field(converter=int)
    connection: socket = field(init=False)

    def __enter__(self) -> socket:
        logging.debug(
            f"Attempting to connect to SQM device at IP {str(self.ip_address)} and port {self.port}"
        )
        self.connection = socket(family=AF_INET, type=SOCK_STREAM)
        self.connection.settimeout(20)
        self.connection.setblocking(False)
        self.connection.connect((self.ip_address, self.port))
        return self.connection

    def __exit__(self):
        self.connection.close()


@define
class PhotometerData:
    """Dataclass for numeric data received from the SQM photometer"""

    temperature: float = field(converter=[_remove_non_digit_characters, float])
    frequency: float = field(converter=[_remove_non_digit_characters, float])
    ticks: float = field(converter=[_remove_non_digit_characters, float])
    sky_brightness: float = field(converter=[_remove_non_digit_characters, float])


@define
class PhotometerMetadata:
    """Dataclass for the metadata from the SQM photometer"""

    protocol_number: int = field(converter=[_remove_non_digit_characters, int])
    model_number: int = field(converter=[_remove_non_digit_characters, int])
    feature_number: int = field(converter=[_remove_non_digit_characters, int])
    serial_number: int = field(converter=[_remove_non_digit_characters, int])


@define
class SQMReader:
    """Reader for the SQM photometer, uses an IPConnection to query an SQM ethernet device and returns either the metadata from the device or the data from the device, depending on functions called"""

    connection: IPConnection = field()

    def read_data(self, tries: int = 1) -> PhotometerData:
        """Reads data from target SQM photometer

        Parameters
        ----------
        tries : int
            Number of tries to connect and download data from the photometer

        Returns
        -------
        PhotometerData
            Photometer data

        """
        data_array = self._read(conn_type="data", tries=tries)
        return PhotometerData(
            temperature=data_array[5],
            frequency=data_array[2],
            ticks=data_array[3],
            sky_brightness=data_array[1],
        )

    def read_metadata(self, tries: int = 1) -> PhotometerMetadata:
        """Reads metadata from target SQM photometer

        Parameters
        ----------
        tries : int
            Number of tries to connect and download data from the photometer

        Returns
        -------
        PhotometerMetadata
            Photometer metadata object

        """
        data_array = self._read(conn_type="metadata", tries=tries)
        return PhotometerMetadata(
            protocol_number=data_array[1],
            model_number=data_array[2],
            feature_number=data_array[3],
            serial_number=data_array[4],
        )

    def _read(
        self, conn_type: Literal["metadata", "calibration", "data"], tries: int = 1
    ) -> List[str]:
        """Given a type of data to retrieve, uses a connection to retrieve target data.

        Parameters
        ----------
        conn_type : Literal["metadata", "calibration", "data"]
            The type of data to retrieve from the SQM photometer
        tries : int
            Number of tries to connect and download data from the photometer

        Returns
        -------
        List[str]
            The received message as a list of strings

        Raises
        ------
        RuntimeError
            If unable to communicate with the photometer, this function will
            throw a Runtime Error as it has failed in its task
        ValueError
            Thrown if given an unknown type of connection

        """

        read_types = {"metadata": "ix", "calibration": "cx", "data": "rx"}
        if conn_type not in read_types:
            raise ValueError(
                f"Received unknown query type {conn_type}, expected one of {', '.join(read_types)}"
            )
        read_command = read_types[conn_type]
        read_verifier = f"{read_command[0]},"
        with self.connection as conn:
            for num in range(tries):
                conn.send(read_command.encode())  # type: ignore

                msg = conn.recv(256).decode()

                try:
                    assert read_verifier in msg
                    logging.debug(f"Received sensor info: {str(msg)}")
                    return msg.split(",")
                except AssertionError:
                    logging.error(
                        f"On try {num} received {msg}. Expected {read_verifier} in message."
                    )

        raise RuntimeError(
            f"Unable to communicate with device, received message {msg}, expected it to contain {read_verifier}"
        )


@define
class SQM:
    reader: SQMReader = field()

    def read_photometer(self, Nmeasures=1, PauseMeasures=2):
        # Initialize values
        temp_sensor = []
        flux_sensor = []
        freq_sensor = []
        ticks_uC = []
        Nremaining = Nmeasures

        # Promediate N measures to remove jitter
        timeutc_initial = datetime.now(timezone.utc)
        while Nremaining > 0:
            InitialDateTime = datetime.now()

            # Get the raw data from the photometer and process it.
            raw_data = self.reader.read_data(tries=10)

            temp_sensor.append(raw_data.temperature)
            freq_sensor.append(raw_data.frequency)
            ticks_uC.append(raw_data.ticks)
            flux_sensor.append(10 ** (-0.4 * raw_data.sky_brightness))
            Nremaining -= 1
            DeltaSeconds = (datetime.now() - InitialDateTime).total_seconds()

            if Nremaining > 0:
                time.sleep(max(1, PauseMeasures - DeltaSeconds))

        timeutc_final = datetime.now(timezone.utc)
        timeutc_delta = timeutc_final - timeutc_initial

        timeutc_mean = timeutc_initial + timedelta(
            seconds=int(timeutc_delta.seconds / 2.0 + 0.5)
        )
        # will convert to local timezone
        timelocal_mean = timeutc_mean.astimezone()

        # Calculate the mean of the data.
        temp_sensor = _filtered_mean(temp_sensor)
        freq_sensor = _filtered_mean(freq_sensor)
        flux_sensor = _filtered_mean(flux_sensor)
        ticks_uC = _filtered_mean(ticks_uC)
        sky_brightness = -2.5 * np.log10(flux_sensor)

        # Correct from offset (if cover is installed on the photometer)
        # sky_brightness = sky_brightness+config._offset_calibration

        return (
            timeutc_mean,
            timelocal_mean,
            temp_sensor,
            freq_sensor,
            ticks_uC,
            sky_brightness,
        )


def make_sqm_reader(ip_address: str, port: int) -> SQM:
    conn = IPConnection(ip_address=ip_address, port=port)
    reader = SQMReader(conn)
    return SQM(reader)
