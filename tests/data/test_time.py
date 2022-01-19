from hypothesis import given, assume
from hypothesis.strategies import floats

from cmt_website.data.time import make_time, ObservatoryTime

import pytest


@given(
    floats(min_value=-180, max_value=180, allow_infinity=False, allow_nan=False),
    floats(min_value=-90, max_value=90, allow_infinity=False, allow_nan=False),
    floats(min_value=0, allow_infinity=False, allow_nan=False),
)
def test_make_time_good(longitude, latitude, height):
    obs_time = make_time(longitude=longitude, latitude=latitude, height=height)
    assert isinstance(obs_time, ObservatoryTime)


@given(floats(), floats(), floats())
def test_make_time_bad(longitude, latitude, height):
    assume(longitude < -180 or longitude > 180)
    assume(latitude < -90 or latitude > 90)
    with pytest.raises(ValueError):
        make_time(longitude=longitude, latitude=latitude, height=height)
